from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView
from swagauth.settings import SWAGAUTH_SETTINGS
from swagconnect.github.connectors import GithubConnector
from swagconnect.oauth2.views import OAuth2LoginView, OAuth2CallbackView

oauth_login = OAuth2LoginView.adapter_view(GithubConnector)
oauth_callback = OAuth2CallbackView.adapter_view(GithubConnector)


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = SWAGAUTH_SETTINGS['github']['CALLBACK_ULR']
    client_class = OAuth2Client
