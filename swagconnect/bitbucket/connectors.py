import json
from urllib.parse import urlparse

import yaml
from rest_framework.exceptions import ValidationError

from swagauth import settings
from swagconnect.api_connector import BaseAPIConnector
from swagconnect.bitbucket.client import BaseBitbucket
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


class BitbucketAPIConnector(BaseBitbucket, BaseAPIConnector):
    def __init__(self, token):
        super(BitbucketAPIConnector, self).__init__(token)

    def get_swagger(self, url: str) -> dict:
        repo_name, branch, path = self._parse_url(url)

        if not self.validate(path):
            raise ValidationError("File content type must be JSON, YAML or YML")

        # repo = self.get_user_repo(repo_name=repo_name)
        print(repo_name, branch, path)
        contents = self.get_swagger_content(repo=repo_name, path=path, ref=branch)
        if path.endswith('json'):
            result = json.loads(contents)
        else:
            result = yaml.safe_load(contents)

        print("\n\n\nRESULT\n", result)
        return result

    def get_swagger_content(self, repo, path, ref=None):
        """
        Return content of the given path file
        :param repo:
        :param path:
        :param ref:
        :return:
        """
        return self.get_bitbucket_content(repo, path)

    def get_user_repo(self, repo_name):
        """
        Return user`s repository
        :param repo_name:
        :return:
        """
        return

    def _parse_url(self, url: str) -> tuple:
        """
        Parse the given url and return repository name, branch and path to the file or directory
        :param url:
        :return: tuple
        """
        # Return repo name, branch name, path to file
        uri = urlparse(url)
        urls = uri.path
        repo_name, path = urls.split('src')

        repo_name, branch = repo_name.strip('/'), path.split('/')[1]
        path = path.replace('/' + branch + '/', '')
        repo_name = repo_name.strip('-')
        repo_name = repo_name.strip('/')
        return repo_name, branch, path


connector_classes = [BitbucketConnector]
