from abc import abstractmethod

from giturlparse import parse

from swag_auth.base import BaseAPIConnector, BaseSwaggerDownloader


class BaseGitAPIConnector(BaseAPIConnector):
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


class BaseGitSwaggerDownloader(BaseSwaggerDownloader):
    api_connector_cls = BaseGitAPIConnector

    def get_swagger_content(self, url, connector):
        owner, repo_name, branch, path = connector._parse_url(url)
        repo = connector.get_user_repo(repo_name=f'{owner}/{repo_name}')

        if not branch:
            branch = connector.get_default_branch(repo)

        return connector.get_file_content(repo=repo, path=path, ref=branch)
