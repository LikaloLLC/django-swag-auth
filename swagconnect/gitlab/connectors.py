import json
from urllib.parse import urlparse

import yaml
from gitlab import Gitlab
from rest_framework.exceptions import ValidationError

from swagauth import settings
from swagconnect.oauth2.views import CustomOAuth2Adapter


class GitlabConnector(CustomOAuth2Adapter):
    provider_id = 'gitlab'

    provider_default_url = "https://gitlab.com"
    provider_api_version = "v4"

    access_token_url = "{0}/oauth/token".format(provider_default_url)
    authorize_url = "{0}/oauth/authorize".format(provider_default_url)
    profile_url = "{0}/api/{1}/user".format(provider_default_url, provider_api_version)

    client_id = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['client_id']
    secret = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['secret']
    scope = settings.SWAGAUTH_SETTINGS[provider_id]['SCOPE']


class GitlabAPIConnector:
    def __init__(self, token):
        # Init python-gitlab here
        self._token = token
        self.client = Gitlab('https://gitlab.com', oauth_token=self._token)

    @classmethod
    def from_credentials(cls, credentials):
        return cls(credentials.token)

    def get_swagger(self, url: str) -> dict:
        repo_name, branch, path = self._parse_url(url)
        if not self.validate(path):
            raise ValidationError("File content type must be JSON, YAML or YML")

        repo = self.client.projects.get(repo_name)
        contents = repo.files.get(file_path=path, ref=branch).decode()
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
        repo_name, path = urls.split('-/blob')
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


connector_classes = [GitlabConnector]
