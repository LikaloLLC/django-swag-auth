from swag_auth.google_drive.connectors import GoogleDriveConnector
from swag_auth.oauth2.views import OAuth2LoginView, OAuth2CallbackView

oauth_login = OAuth2LoginView.adapter_view(GoogleDriveConnector)
oauth_callback = OAuth2CallbackView.adapter_view(GoogleDriveConnector)
