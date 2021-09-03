import re
from django.conf import settings

from swag_auth.base import BaseAPIConnector, BaseSwaggerDownloader
from swag_auth.confluence.client import Client
from swag_auth.oauth2.views import CustomOAuth2Adapter


class ConfluenceAPIConnector(BaseAPIConnector):
    def __init__(self, email, token, domain):
        super().__init__(token)
        self.email = email
        self.domain = domain
        self.client = Client(self.email, token, self.domain)

    def get_file_content(self, page_id: int):
        return self.client.get_page_html(page_id=page_id)

    def __str__(self):
        return "ConfluenceAPIConnector"


class ConfluenceSwaggerDownloader(BaseSwaggerDownloader):
    api_connector_cls = ConfluenceAPIConnector

    def __init__(self, email, token, domain):
        self.email = email
        self.domain = domain
        super().__init__(token)
        self.token = token

    def get_api_connector(self):
        return self.api_connector_cls(self.email, self._token, self.domain)

    def get_swagger_content(self, url: str, connector: 'ConfluenceAPIConnector'):
        page_id = self.get_page_id(url)

        return connector.get_file_content(page_id=page_id)

    def get_page_id(self, url: str) -> int:
        pattern = re.compile('/pages/([\d-])/')
        a = pattern.search(url)
        return 98472


class ConfluenceConnector(CustomOAuth2Adapter):
    provider_id = 'confluence'
    access_token_url = "https://auth.atlassian.com/oauth/token"
    authorize_url = "https://auth.atlassian.com/authorize"
    audience = 'api.atlassian.com'
    client_id = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['client_id']
    secret = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['secret']
    scope = settings.SWAGAUTH_SETTINGS[provider_id]['SCOPE']

    api_connector_class = ConfluenceSwaggerDownloader


connector_classes = [ConfluenceConnector]
