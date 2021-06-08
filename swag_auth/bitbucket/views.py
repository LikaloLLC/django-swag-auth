from swag_auth.bitbucket.connectors import BitbucketConnector
from swag_auth.oauth2.views import OAuth2LoginView, OAuth2CallbackView

oauth_login = OAuth2LoginView.adapter_view(BitbucketConnector)
oauth_callback = OAuth2CallbackView.adapter_view(BitbucketConnector)
