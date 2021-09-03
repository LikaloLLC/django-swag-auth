from swag_auth.confluence.connectors import ConfluenceConnector
from swag_auth.oauth2.views import OAuth2LoginView, OAuth2CallbackView

oauth2_login = OAuth2LoginView.adapter_view(ConfluenceConnector)
oauth2_callback = OAuth2CallbackView.adapter_view(ConfluenceConnector)
