from django.conf import settings
from github import Github

from swagconnect.oauth2.views import CustomOAuth2Adapter


class GithubConnector(CustomOAuth2Adapter):
    """
    Github connector
    """
    provider_id = 'github'

    client_id = settings.SWAGAUTH_SETTINGS['github']['APP']['client_id']
    secret = settings.SWAGAUTH_SETTINGS['github']['APP']['secret']

    access_token_url = "https://github.com/login/oauth/access_token"
    authorize_url = "https://github.com/login/oauth/authorize"
    profile_url = "https://api.github.com/user"
    emails_url = "https://api.github.com/user/emails"
    scope = settings.SWAGAUTH_SETTINGS['github']['SCOPE']

    def store_credentials(self, request, token):
        pass


class GithubAPIConnector:
    def __init__(self, token):
        # Init PyGithub here
        self._token = token
        self.client = Github(self._token)

    @classmethod
    def from_credentials(cls, credentials):
        return cls(credentials.token)

    def get_swagger(self, url: str) -> dict:
        repo_name, branch, path = self._parse_url(url)

    def _parse_url(self, url: str) -> str:
        """Parse the given url and return repository name, branch and path to the file or direcotry"""

        # Return repo name, branch name, path to file
