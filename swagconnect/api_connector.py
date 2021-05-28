import json
from urllib.parse import urlparse

import yaml
from gitlab import Gitlab
from rest_framework.exceptions import ValidationError


class BaseAPIConnector:
    def __init__(self, token):
        self._token = token


    @classmethod
    def from_credentials(cls, credentials):
        return cls(credentials.token)

    def get_swagger(self, url: str) -> dict:
        repo_name, branch, path = self._parse_url(url)

        if not self.validate(path):
            raise ValidationError("File content type must be JSON, YAML or YML")

        repo = self.get_user_repo(repo_name=repo_name)
        contents = self.get_swagger_content(repo=repo, path=path, ref=branch)
        if path.endswith('json'):
            result = json.loads(contents)
        else:
            result = yaml.safe_load(contents)
        return result

    def get_swagger_content(self, repo, path, ref=None):
        """
        Return content of the given path file
        :param repo:
        :param path:
        :param ref:
        :return:
        """
        raise NotImplementedError

    def get_user_repo(self, repo_name):
        """
        Return user`s repository
        :param repo_name:
        :return:
        """
        raise NotImplementedError

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
        repo_name = repo_name.strip('-')
        repo_name = repo_name.strip('/')
        return repo_name, branch, path

    def validate(self, path: str) -> bool:
        """
        Validate path to YAML or JSON
        :param path:
        :return: bool:
        """
        path = path.lower()
        return path.endswith('json') or path.endswith('yml') or path.endswith('yaml')
