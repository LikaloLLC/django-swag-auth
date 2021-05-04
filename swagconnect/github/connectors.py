from django.conf import settings

from swagconnect.oauth2.views import CustomOAuth2Adapter


class GithubConnector(CustomOAuth2Adapter):
    id = 'github'

    # TODO: Better implementation of getting secrets
    client_id = settings.SWAGAUTH_SETTINGS['github']['APP']['client_id']
    secret = settings.SWAGAUTH_SETTINGS['github']['APP']['secret']

    access_token_url = "https://github.com/login/oauth/access_token"
    authorize_url = "https://github.com/login/oauth/authorize"
    profile_url = "https://api.github.com/user"
    emails_url = "https://api.github.com/user/emails"