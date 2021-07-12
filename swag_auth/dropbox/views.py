from swag_auth.dropbox.connectors import DropboxConnector
from swag_auth.oauth2.views import OAuth2LoginView, OAuth2CallbackView

oauth2_login = OAuth2LoginView.adapter_view(DropboxConnector)
oauth2_callback = OAuth2CallbackView.adapter_view(DropboxConnector)
