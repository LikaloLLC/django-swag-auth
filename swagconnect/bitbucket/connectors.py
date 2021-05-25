from swagauth import settings
from swagconnect.oauth2.views import CustomOAuth2Adapter


class BitbucketConnector(CustomOAuth2Adapter):
    provider_id = 'bitbucket'
    access_token_url = "https://bitbucket.org/site/oauth2/access_token"
    authorize_url = "https://bitbucket.org/site/oauth2/authorize"
    profile_url = "https://api.bitbucket.org/2.0/user"
    emails_url = "https://api.bitbucket.org/2.0/user/emails"
    client_id = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['key']
    secret = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['secret']
    scope = settings.SWAGAUTH_SETTINGS[provider_id]['SCOPE']


connector_classes = [BitbucketConnector]
