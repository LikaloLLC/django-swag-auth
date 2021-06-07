from swag_auth.swagconnect.github.connectors import GithubConnector
from swag_auth.swagconnect.oauth2.views import OAuth2LoginView, OAuth2CallbackView

oauth_login = OAuth2LoginView.adapter_view(GithubConnector)
oauth_callback = OAuth2CallbackView.adapter_view(GithubConnector)


