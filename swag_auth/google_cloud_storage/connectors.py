from urllib.parse import urlparse, unquote

from django.conf import settings
from google.cloud import storage
from google.oauth2.credentials import Credentials

from swag_auth.base import BaseAPIConnector, BaseSwaggerDownloader
from swag_auth.oauth2.views import CustomOAuth2Adapter


class GoogleCloudStorageAPIConnector(BaseAPIConnector):
    def __init__(self, token):
        super().__init__(token)

        credentials = Credentials(token=token)
        self.client = storage.Client(credentials=credentials)

    def get_file_content(self, bucket_name: str, filename: str):
        # See the https://cloud.google.com/storage/docs/downloading-objects#code-samples
        bucket = self.client.get_bucket(bucket_name)
        blob = bucket.blob(filename)

        return blob.download_as_string()


class GoogleCloudStorageSwaggerDownloader(BaseSwaggerDownloader):
    api_connector_cls = GoogleCloudStorageAPIConnector

    def get_swagger_content(self, url: str, connector: 'GoogleCloudStorageAPIConnector'):
        url = unquote(url)
        bucket_name = self.get_bucket_name(url)
        filename = self.get_filename(url)

        return connector.get_file_content(bucket_name, filename)

    def get_bucket_name(self, url: str) -> str:
        """Parse authenticated Google Cloud Storage URL and return bucket name."""
        obj = urlparse(url)
        return obj.path.lstrip('/').split('/', maxsplit=1)[0]

    def get_filename(self, url: str) -> str:
        """Parse authenticated Google Cloud Storage URL and return full filename, including path."""
        obj = urlparse(url)
        return obj.path.lstrip('/').split('/', maxsplit=1)[1]


class GoogleCloudStorageConnector(CustomOAuth2Adapter):
    provider_id = 'google_cloud_storage'

    client_id = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['client_id']
    secret = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['secret']

    access_token_url = "https://accounts.google.com/o/oauth2/token"
    authorize_url = "https://accounts.google.com/o/oauth2/auth"
    profile_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    scope = settings.SWAGAUTH_SETTINGS[provider_id]['SCOPE']

    api_connector_class = GoogleCloudStorageSwaggerDownloader


connector_classes = [GoogleCloudStorageConnector]
