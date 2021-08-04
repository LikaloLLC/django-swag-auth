import os
from urllib.parse import urlparse

from boxsdk import OAuth2, Client
from django.conf import settings

from swag_auth.base import BaseSwaggerDownloader, BaseAPIConnector
from swag_auth.oauth2.views import CustomOAuth2Adapter


class BoxAPIConnector(BaseAPIConnector):
    def __init__(self, token):
        super().__init__(token)

        auth = OAuth2(
            client_id=settings.SWAGAUTH_SETTINGS['box']['APP']['client_id'],
            client_secret=settings.SWAGAUTH_SETTINGS['box']['APP']['secret'],
            access_token=token,
        )
        self.client = Client(auth)

    def get_file_content(self, file_id: str):
        return self.client.file(file_id).content()

    def get_file_information(self, file_id: str):
        return self.client.file(file_id).get()


class BoxSwaggerDownloader(BaseSwaggerDownloader):
    api_connector_cls = BoxAPIConnector

    def get_swagger_content(self, url: str, connector: 'BoxAPIConnector'):
        file_id = self.get_file_id(url)

        return connector.get_file_content(file_id)

    def get_extension(self, url: str) -> str:
        file_id = self.get_file_id(url)
        connector = self.get_api_connector()
        file = connector.get_file_information(file_id)

        return os.path.splitext(file.name)[1][1:]

    def get_file_id(self, url: str) -> str:
        return urlparse(url).path.lstrip('/').split('/')[1]


class BoxConnector(CustomOAuth2Adapter):
    provider_id = 'box'
    access_token_url = "https://api.box.com/oauth2/token"
    authorize_url = "https://account.box.com/api/oauth2/authorize"
    profile_url = "https://api.box.com/2.0/users/me"

    client_id = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['client_id']
    secret = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['secret']
    scope = settings.SWAGAUTH_SETTINGS[provider_id]['SCOPE']

    api_connector_class = BoxSwaggerDownloader


connector_classes = [BoxConnector]
