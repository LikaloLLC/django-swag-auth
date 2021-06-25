import json
import os
from abc import ABC, abstractmethod
from typing import Union

import yaml
from giturlparse import parse
from rest_framework.exceptions import ValidationError


class BaseGitAPIConnector(ABC):
    def __init__(self, token):
        self._token = token

    @classmethod
    def from_credentials(cls, credentials):
        return cls(credentials.token)

    @abstractmethod
    def get_file_content(self, repo, path, ref):
        """
        Return content of the given path file
        :param repo:
        :param path:
        :param ref:
        :return:
        """
        pass

    @abstractmethod
    def get_user_repo(self, repo_name):
        """
        Return user`s repository
        :param repo_name:
        :return:
        """
        pass

    @abstractmethod
    def get_default_branch(self, repo) -> str:
        """
        Return repository's default branch
        :param repo:
        :return: branch:
        :rtype: str:
        """
        pass

    def _parse_url(self, url: str) -> tuple:
        """
        Parse the given url and return repository name, branch and path to the file or directory
        :param url:
        :return: tuple
        """
        # Return repo name, branch name, path to file
        p = parse(url)
        repo_name = p.repo
        owner = p.owner
        b = p.branch
        if b:
            branch = b.split('/', 1)[0]
            path = b.replace(f'{branch}/', '')
        else:
            branch = p.path.split('/', 1)[0]
            path = p.path.replace(f"{branch}/", '')

        if repo_name == '-':
            repo_name = p.data.get('groups_path')

        return owner, repo_name, branch, path


class BaseGitSwaggerDownloader(BaseGitAPIConnector, ABC):
    # A mapping of extension name to a real loader
    loaders = {
        'json': json.loads,
        'yml': yaml.safe_load,
        'yaml': yaml.safe_load
    }

    def get_swagger_data(self, path: str, contents: Union[str, bytes]):
        extension = os.path.splitext(path)[1][1:]

        return self.loaders[extension](contents)

    def get_swagger(self, url: str) -> dict:
        owner, repo_name, branch, path = self._parse_url(url)

        if not self.is_path_valid(path):
            raise ValidationError("File content type must be JSON, YAML or YML")

        repo = self.get_user_repo(repo_name=f'{owner}/{repo_name}')

        if not branch:
            branch = self.get_default_branch(repo)

        contents = self.get_file_content(repo=repo, path=path, ref=branch)

        return self.get_swagger_data(path, contents)

    def is_path_valid(self, path: str) -> bool:
        """
        Validate path to YAML or JSON
        :param path:
        :return: bool:
        """
        extension = os.path.splitext(path)[1][1:]
        return extension in self.loaders
