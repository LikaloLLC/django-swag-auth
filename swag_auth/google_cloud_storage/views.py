from swag_auth.google_cloud_storage.connectors import GoogleCloudStorageConnector
from swag_auth.oauth2.views import OAuth2LoginView, OAuth2CallbackView

oauth2_login = OAuth2LoginView.adapter_view(GoogleCloudStorageConnector)
oauth2_callback = OAuth2CallbackView.adapter_view(GoogleCloudStorageConnector)
