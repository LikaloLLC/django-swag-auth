from django.conf import settings
from gitlab import Gitlab

from swag_auth.api_connector import BaseGitSwaggerDownloader, BaseGitAPIConnector
from swag_auth.oauth2.views import CustomOAuth2Adapter


class GitlabAPIConnector(BaseGitAPIConnector):
    def __init__(self, token):
        super().__init__(token)

        self.client = Gitlab("https://gitlab.com", oauth_token=self._token)

    def get_file_content(self, repo, path, ref):
        """
        Return content of the given path file
        :param repo:
        :param path:
        :param ref:
        :return:
        """
        return repo.files.get(file_path=path, ref=ref).decode()

    def get_user_repo(self, repo_name):
        """
        Return user`s repository
        :param repo_name:
        :return:
        """
        return self.client.projects.get(repo_name)

    def get_default_branch(self, repo) -> str:
        return repo.default_branch


class GitlabSwaggerDownloader(BaseGitSwaggerDownloader):
    api_connector_cls = GitlabAPIConnector


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

    api_connector_class = GitlabSwaggerDownloader


connector_classes = [GitlabConnector]
