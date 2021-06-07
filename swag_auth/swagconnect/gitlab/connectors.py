from gitlab import Gitlab

from swagauth import settings
from swag_auth.swagconnect.api_connector import BaseAPIConnector
from swag_auth.swagconnect.oauth2.views import CustomOAuth2Adapter


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


class GitlabAPIConnector(BaseAPIConnector):
    def __init__(self, token):
        super(GitlabAPIConnector, self).__init__(token)
        self.client = Gitlab("https://gitlab.com", oauth_token=self._token)

    def get_swagger_content(self, repo, path, ref=None):
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


connector_classes = [GitlabConnector]
