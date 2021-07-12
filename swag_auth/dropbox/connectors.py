import os
import re
from urllib.parse import urlparse, unquote, parse_qs

from django.conf import settings
from dropbox import Dropbox

from swag_auth.base import BaseAPIConnector, BaseSwaggerDownloader
from swag_auth.oauth2.views import CustomOAuth2Adapter


class DropboxAPIConnector(BaseAPIConnector):
    def __init__(self, token):
        super().__init__(token)

        self.client = Dropbox(token)

    def get_file_content(self, path: str):
        # Dropbox' related method documentation:
        # https://dropbox-sdk-python.readthedocs.io/en/latest/api/dropbox.html#dropbox.dropbox_client.Dropbox.files_download
        metadata, response = self.client.files_download(path=path)
        return response.content

    def get_shared_file_content(self, shared_link: str):
        # Dropbox' related method documentation:
        # https://dropbox-sdk-python.readthedocs.io/en/latest/api/dropbox.html#dropbox.dropbox_client.Dropbox.sharing_get_shared_link_file
        metadata, response = self.client.sharing_get_shared_link_file(url=shared_link)
        return response.content


class DropboxSwaggerDownloader(BaseSwaggerDownloader):
    api_connector_cls = DropboxAPIConnector

    def get_swagger_content(self, url: str, connector: 'DropboxAPIConnector'):
        if self.is_shared_link(url):
            return connector.get_shared_file_content(url)

        url = unquote(url)
        path = self.get_path(url)
        return connector.get_file_content(path)

    def is_shared_link(self, url: str) -> bool:
        pattern = re.compile('/s/([\w-]{14,15})/')
        return bool(pattern.search(url))

    def get_path(self, url: str) -> str:
        return url.split('home')[1].replace('?preview=', '/')

    def get_extension(self, url: str) -> str:
        if self.is_shared_link(url):
            return os.path.splitext(urlparse(url).path)[1][1:]
        filename = parse_qs(urlparse(url).query)['preview']
        return os.path.splitext(filename[0])[1][1:]


class DropboxConnector(CustomOAuth2Adapter):
    """
    Github connector
    """
    provider_id = 'dropbox'

    client_id = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['client_id']
    secret = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['secret']

    access_token_url = "https://api.dropbox.com/oauth2/token"
    authorize_url = "https://www.dropbox.com/oauth2/authorize"
    profile_url = "https://api.dropbox.com/2/users/get_current_account"
    scope = settings.SWAGAUTH_SETTINGS[provider_id]['SCOPE']

    api_connector_class = DropboxSwaggerDownloader


connector_classes = [DropboxConnector]
