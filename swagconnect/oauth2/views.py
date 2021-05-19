from datetime import timedelta

from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.helpers import (render_authentication_error)
from allauth.socialaccount.models import SocialLogin, SocialToken
from allauth.socialaccount.providers.base import AuthError, ProviderException
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from allauth.utils import get_request_param
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.utils import timezone
from requests import RequestException

from swagconnect.helpers import complete_authentication
from swagconnect.models import ConnectorToken


class CustomOAuth2Adapter(OAuth2Adapter):
    provider_id = None
    client_id = None
    secret = None
    access_token_url = None
    authorize_url = None
    profile_url = None
    emails_url = None
    scope = []
    callback_url = None

    def complete_login(self, request, app, access_token, **kwargs):
        return

    def get_provider(self):
        return

    def parse_token(self, data):
        token = SocialToken(token=data["access_token"])
        token.token_secret = data.get("refresh_token", "")
        expires_in = data.get(self.expires_in_key, None)
        if expires_in:
            token.expires_at = timezone.now() + timedelta(seconds=int(expires_in))
        return token

    def get_access_token_data(self, request, app, client):
        code = get_request_param(self.request, "code")
        return client.get_access_token(code)

    def store_credentials(self, request, token, token_secret=None, expires_at=None):
        """
        Save credentials in the ConnectorToken model.
        :param request:
        :param token:
        :param token_secret:
        :param expires_at:
        :return:
        """
        return ConnectorToken.objects.create(
            connector=self.provider_id,
            token=token,
            token_secret=token_secret,
            expires_at=expires_at
        )


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
        scope = self.adapter.scope
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
            return HttpResponseRedirect(client.get_redirect_url(auth_url, {}))
        except OAuth2Error as e:
            return render_authentication_error(request, self.adapter.provider_id, exception=e)


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
        client = self.get_client(request, None)
        try:
            access_token = self.adapter.get_access_token_data(request, None, client)
            token = self.adapter.parse_token(access_token)
            self.adapter.store_credentials(request=request, token=token.token, token_secret=token.token_secret)
            return complete_authentication(request, token)
        except (
                PermissionDenied,
                OAuth2Error,
                RequestException,
                ProviderException,
        ) as e:
            return render_authentication_error(
                request, self.adapter.provider_id, exception=e
            )
