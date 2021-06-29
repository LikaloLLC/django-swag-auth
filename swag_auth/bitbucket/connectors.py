from urllib.parse import urlparse

from atlassian.bitbucket.cloud import Cloud
from django.conf import settings

from swag_auth.api_connector import BaseGitSwaggerDownloader
from swag_auth.bitbucket.client import BitbucketAPIClient
from swag_auth.oauth2.views import CustomOAuth2Adapter


class BitbucketSwaggerDownloader(BaseGitSwaggerDownloader):
    def __init__(self, token):
        super().__init__(token)

        self.client = BitbucketAPIClient(self._token)
        token = {
            'access_token': token,
            'token_type': 'bearer'
        }
        oauth2_dict = {
            "client_id": settings.SWAGAUTH_SETTINGS['bitbucket']['APP']['key'],
            "token": token}
        self.cloud = Cloud(
            url='https://api.bitbucket.org/',
            oauth2=oauth2_dict
        )

    def get_file_content(self, repo, path, ref):
        """
        Return content of the given path file
        :param repo:
        :param path:
        :param ref:
        :return:
        """
        return self.client.get_content(repo, path, ref)

    def get_user_repo(self, repo_name):
        """
        Return user`s repository
        :param repo_name:
        :return:
        """
        return repo_name

    def get_default_branch(self, repo) -> str:
        repo, branch = repo.split('/', 1)[0], ''
        repository = self.cloud.repositories.get(repo)
        branch = repository['values'][0]['mainbranch']['name']
        return branch

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
        repo_name = repo_name.strip('-').strip('/')
        owner, repo_name = repo_name.split('/')
        return owner, repo_name, branch, path


class BitbucketConnector(CustomOAuth2Adapter):
    provider_id = 'bitbucket'
    access_token_url = "https://bitbucket.org/site/oauth2/access_token"
    authorize_url = "https://bitbucket.org/site/oauth2/authorize"
    profile_url = "https://api.bitbucket.org/2.0/user"
    emails_url = "https://api.bitbucket.org/2.0/user/emails"
    client_id = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['key']
    secret = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['secret']
    scope = settings.SWAGAUTH_SETTINGS[provider_id]['SCOPE']

    api_connector_class = BitbucketSwaggerDownloader


connector_classes = [BitbucketConnector]
