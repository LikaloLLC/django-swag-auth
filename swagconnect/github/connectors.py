import json
from urllib.parse import urlparse

import yaml
from django.conf import settings
from django.core.exceptions import ValidationError
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

    def store_credentials(self, request, token, token_secret=None, expires_at=None):
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
        if not self.validate(path):
            raise ValidationError("File content type must be JSON, YAML or YML")

        repo = self.client.get_repo(full_name_or_id=repo_name)
        contents = repo.get_contents(path).decoded_content.decode()
        if path.endswith('json'):
            result = json.loads(contents)
        else:
            result = yaml.safe_load(contents)
        return result

    def _parse_url(self, url: str) -> tuple:
        """
        Parse the given url and return repository name, branch and path to the file or directory
        :param url:
        :return: tuple
        """

        # Return repo name, branch name, path to file
        uri = urlparse(url)
        urls = uri.path
        repo_name, path = urls.split('blob')
        repo_name, branch = repo_name.strip('/'), path.split('/')[1]
        path = path.replace('/' + branch + '/', '')
        return repo_name, branch, path

    def validate(self, path: str) -> bool:
        """
        Validate path to YAML or JSON
        :param path:
        :return: bool:
        """
        path = path.lower()
        return path.endswith('json') or path.endswith('yml') or path.endswith('yaml')
