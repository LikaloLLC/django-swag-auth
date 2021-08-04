from swag_auth.box.connectors import BoxConnector
from swag_auth.oauth2.views import OAuth2LoginView, OAuth2CallbackView

oauth2_login = OAuth2LoginView.adapter_view(BoxConnector)
oauth2_callback = OAuth2CallbackView.adapter_view(BoxConnector)
