from swag_auth.gitlab.connectors import GitlabConnector
from swag_auth.oauth2.views import OAuth2LoginView, OAuth2CallbackView

oauth2_login = OAuth2LoginView.adapter_view(GitlabConnector)
oauth2_callback = OAuth2CallbackView.adapter_view(GitlabConnector)
