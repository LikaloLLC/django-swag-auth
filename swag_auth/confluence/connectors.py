from atlassian import Confluence
from django.conf import settings

from swag_auth.base import BaseAPIConnector, BaseSwaggerDownloader


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
        self.client = Confluence(url='', oauth2=oauth2_dict)

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
