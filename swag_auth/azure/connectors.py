from django.conf import settings

from swag_auth.azure.client import AzureBlobStorage
from swag_auth.base import BaseAPIConnector, BaseSwaggerDownloader
from swag_auth.oauth2.views import CustomOAuth2Adapter


class AzureAPIConnector(BaseAPIConnector):
    def __init__(self, token):
        super().__init__(token)
        self.client = AzureBlobStorage(token)

    def get_file_content(self, url):
        """
        Return content of the given path file
        """
        return self.client.get_content(url)


class AzureSwaggerDownloader(BaseSwaggerDownloader):
    api_connector_cls = AzureAPIConnector

    def get_swagger_content(self, url: str, connector: 'AzureAPIConnector'):
        return connector.get_file_content(url)


class AzureConnector(CustomOAuth2Adapter):
    provider_id = 'azure'
    access_token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    authorize_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
    profile_url = "https://graph.microsoft.com/v1.0/me"
    groups_url = "https://graph.microsoft.com/v1.0/me/memberOf?$select=displayName"

    client_id = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['client_id']
    secret = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['secret']
    scope = settings.SWAGAUTH_SETTINGS[provider_id]['SCOPE']

    api_connector_class = AzureSwaggerDownloader


connector_classes = [AzureConnector]
