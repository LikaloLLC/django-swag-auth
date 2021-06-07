from django.conf import settings
from github import Github

from swag_auth.api_connector import BaseAPIConnector
from swag_auth.oauth2.views import CustomOAuth2Adapter


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


class GithubAPIConnector(BaseAPIConnector):
    def __init__(self, token):
        super(GithubAPIConnector, self).__init__(token)
        self.client = Github(self._token)

    def get_swagger_content(self, repo, path, ref=None):
        """
        Return content of the given path file
        :param repo:
        :param path:
        :param ref:
        :return:
        """
        return repo.get_contents(path).decoded_content.decode()

    def get_user_repo(self, repo_name):
        """
        Return user`s repository
        :param repo_name:
        :return:
        """
        return self.client.get_repo(full_name_or_id=repo_name)


connector_classes = [GithubConnector]
