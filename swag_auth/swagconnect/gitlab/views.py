from swag_auth.swagconnect.gitlab.connectors import GitlabConnector
from swag_auth.swagconnect.oauth2.views import OAuth2LoginView, OAuth2CallbackView

oauth_login = OAuth2LoginView.adapter_view(GitlabConnector)
oauth_callback = OAuth2CallbackView.adapter_view(GitlabConnector)
