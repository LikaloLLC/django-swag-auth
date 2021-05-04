from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.helpers import (render_authentication_error, complete_social_login)
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.base import AuthError, ProviderException
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from allauth.utils import get_request_param

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

from requests import RequestException


class CustomOAuth2Adapter(OAuth2Adapter):
  def complete_login(self, request, app, access_token, **kwargs):
    return

  def get_provider(self):
    return


class OAuth2View(object):
  @classmethod
  def adapter_view(cls, adapter):
    def view(request, *args, **kwargs):
      self = cls()
      self.request = request
      self.adapter = adapter(request)
      try:
        return self.dispatch(request, *args, **kwargs)
      except ImmediateHttpResponse as e:
        return e.response

    return view

  def get_client(self, request, app):
    callback_url = self.adapter.get_callback_url(request, None)
    scope = self.adapter.get_scope(request)
    client = self.adapter.client_class(
      self.request,
      self.adapter.client_id,
      self.adapter.secret,
      self.adapter.access_token_method,
      self.adapter.access_token_url,
      callback_url,
      scope,
      scope_delimiter=self.adapter.scope_delimiter,
      headers=self.adapter.headers,
      basic_auth=self.adapter.basic_auth,
    )
    return client


class OAuth2LoginView(OAuth2View):
  def dispatch(self, request, *args, **kwargs):
    client = self.get_client(request, None)
    auth_url = self.adapter.authorize_url
    client.state = SocialLogin.stash_state(request)
    try:
      return HttpResponseRedirect(client.get_redirect_url(auth_url, None))
    except OAuth2Error as e:
      return render_authentication_error(request, self.adapter.id, exception=e)


class OAuth2CallbackView(OAuth2View):
  def dispatch(self, request, *args, **kwargs):
    if "error" in request.GET or "code" not in request.GET:
      # Distinguish cancel from error
      auth_error = request.GET.get("error", None)
      if auth_error == self.adapter.login_cancelled_error:
        error = AuthError.CANCELLED
      else:
        error = AuthError.UNKNOWN
      return render_authentication_error(
        request, self.adapter.provider_id, error=error
      )
    client = self.get_client(self.request, None)

    try:
      access_token = self.adapter.get_access_token_data(request, None, client)
      token = self.adapter.parse_token(access_token)
      login = self.adapter.complete_login(
        request, None, token, response=access_token
      )
      login.token = token
      if self.adapter.supports_state:
        login.state = SocialLogin.verify_and_unstash_state(
          request, get_request_param(request, "state")
        )
      else:
        login.state = SocialLogin.unstash_state(request)

      return complete_social_login(request, login)
    except (
      PermissionDenied,
      OAuth2Error,
      RequestException,
      ProviderException,
    ) as e:
      return render_authentication_error(
        request, self.adapter.id, exception=e
      )
