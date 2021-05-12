from swagconnect.bitbucket.connectors import BitbucketConnector
from swagconnect.oauth2.views import OAuth2LoginView, OAuth2CallbackView

oauth_login = OAuth2LoginView.adapter_view(BitbucketConnector)
oauth_callback = OAuth2CallbackView.adapter_view(BitbucketConnector)
