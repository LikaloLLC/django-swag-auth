from atlassian import Confluence
from django.conf import settings

from swag_auth.base import BaseAPIConnector, BaseSwaggerDownloader
from swag_auth.oauth2.views import CustomOAuth2Adapter


class ConfluenceAPIConnector(BaseAPIConnector):
    def __init__(self, token):
        super().__init__(token)
        token = {
            'access_token': token,
            'token_type': 'Bearer'
        }
        oauth2_dict = {
            "client_id": settings.SWAGAUTH_SETTINGS['confluence']['APP']['client_id'],
            "token": token}
        self.client = Confluence(url='https://api.atlassian.com', oauth2=oauth2_dict)

    def get_file_content(self, path: str):
        return


class ConfluenceSwaggerDownloader(BaseSwaggerDownloader):
    api_connector_cls = ConfluenceAPIConnector

    def get_swagger_content(self, url: str, connector: 'ConfluenceAPIConnector'):
        ...

    def get_path(self, url: str) -> str:
        ...

    def get_extension(self, url: str) -> str:
        ...


class ConfluenceConnector(CustomOAuth2Adapter):
    provider_id = 'confluence'
    access_token_url = "https://auth.atlassian.com/oauth/token"
    authorize_url = "https://auth.atlassian.com/authorize"
    client_id = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['client_id']
    secret = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['secret']
    scope = settings.SWAGAUTH_SETTINGS[provider_id]['SCOPE']
    callback_url = 'http://127.0.0.1:8000/swag/confluence/login/callback/'

    api_connector_class = ConfluenceSwaggerDownloader


connector_classes = [ConfluenceConnector]
