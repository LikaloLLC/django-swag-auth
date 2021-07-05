from django.conf import settings
from github import Github

from swag_auth.api_connector import BaseGitSwaggerDownloader, BaseGitAPIConnector
from swag_auth.oauth2.views import CustomOAuth2Adapter


class GithubAPIConnector(BaseGitAPIConnector):
    def __init__(self, token):
        super().__init__(token)

        self.client = Github(self._token)

    def get_file_content(self, repo, path, ref):
        """
        Return content of the given path file
        :param repo:
        :param path:
        :param ref:
        :return:
        """
        return repo.get_contents(path, ref=ref).decoded_content.decode()

    def get_user_repo(self, repo_name):
        """
        Return user`s repository
        :param repo_name:
        :return:
        """
        return self.client.get_repo(full_name_or_id=repo_name)

    def get_default_branch(self, repo) -> str:
        return repo.default_branch


class GithubSwaggerDownloader(BaseGitSwaggerDownloader):
    api_connector_cls = GithubAPIConnector


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

    api_connector_class = GithubSwaggerDownloader


connector_classes = [GithubConnector]
