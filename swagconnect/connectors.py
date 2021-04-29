from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter


class CustomOAuth2Adapter(OAuth2Adapter):
    def complete_login(self, request, app, access_token, **kwargs):
        return


class BitbucketConnector(CustomOAuth2Adapter):
    id = 'bitbucket'
    access_token_url = "https://bitbucket.org/site/oauth2/access_token"
    authorize_url = "https://bitbucket.org/site/oauth2/authorize"
    profile_url = "https://api.bitbucket.org/2.0/user"
    emails_url = "https://api.bitbucket.org/2.0/user/emails"


class GithubConnector(CustomOAuth2Adapter):
    id = 'github'


class GitlabConnector(CustomOAuth2Adapter):
    id = 'gitlab'
