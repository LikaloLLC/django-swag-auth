from swag_auth.base import BaseAPIConnector, BaseSwaggerDownloader
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


class GoogleDriveAPIConnector(BaseAPIConnector):
    def __init__(self, token):
        super().__init__(token)

        credentials = Credentials(token=token)
        self.client = build('drive', 'v3', credentials=credentials)

    def get_file_content(self, file_id: str):
        pass


class GoogleDriveSwaggerDownloader(BaseSwaggerDownloader):
    api_connector_cls = GoogleDriveAPIConnector

    def get_swagger_content(self, url: str, connector: 'GoogleDriveAPIConnector'):
        pass

    def get_file_id(self, url: str) -> str:
        pass

    def get_extension(self, url):
        # This should be overridden, because google url does not have an extension
        pass
