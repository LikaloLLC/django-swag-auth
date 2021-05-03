from swagconnect.oauth2.views import CustomOAuth2Adapter


class BitbucketConnector(CustomOAuth2Adapter):
    id = 'bitbucket'
    access_token_url = "https://bitbucket.org/site/oauth2/access_token"
    authorize_url = "https://bitbucket.org/site/oauth2/authorize"
    profile_url = "https://api.bitbucket.org/2.0/user"
    emails_url = "https://api.bitbucket.org/2.0/user/emails"
