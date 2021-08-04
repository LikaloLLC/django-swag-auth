from swag_auth.azure.connectors import AzureConnector
from swag_auth.oauth2.views import OAuth2LoginView, OAuth2CallbackView

oauth2_login = OAuth2LoginView.adapter_view(AzureConnector)
oauth2_callback = OAuth2CallbackView.adapter_view(AzureConnector)
