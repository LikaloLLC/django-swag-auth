import io

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from conf import settings
from swag_auth.base import BaseAPIConnector, BaseSwaggerDownloader
from swag_auth.oauth2.views import CustomOAuth2Adapter


class GoogleDriveAPIConnector(BaseAPIConnector):
    def __init__(self, token):
        super().__init__(token)

        credentials = Credentials(token=token)
        self.client = build('drive', 'v3', credentials=credentials)

    def get_file_content(self, file_id: str):
        file = self.client.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, file)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        return fh.getvalue()



class GoogleDriveSwaggerDownloader(BaseSwaggerDownloader):
    api_connector_cls = GoogleDriveAPIConnector

    def get_swagger_content(self, url: str, connector: 'GoogleDriveAPIConnector'):
        file_id = self.get_file_id(url)
        return connector.get_file_content(file_id)

    def get_file_id(self, url: str) -> str:
        return url.split('/')[5]

    def get_extension(self, url: str) -> str:
        # This should be overridden, because google url does not have an extension
        file_id = self.get_file_id(url)
        connector = self.get_api_connector()
        return connector.client.files().get(fileId=file_id).execute().get('mimeType').split('/')[1]


class GoogleDriveConnector(CustomOAuth2Adapter):
    """
    Google Drive connector
    """
    provider_id = 'google'

    client_id = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['client_id']
    secret = settings.SWAGAUTH_SETTINGS[provider_id]['APP']['secret']

    access_token_url = "https://accounts.google.com/o/oauth2/token"
    authorize_url = "https://accounts.google.com/o/oauth2/auth"
    profile_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    scope = settings.SWAGAUTH_SETTINGS[provider_id]['SCOPE']

    api_connector_class = GoogleDriveSwaggerDownloader


connector_classes = [GoogleDriveConnector]
