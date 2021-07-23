import requests


class AzureBlobStorage:
    """
    Get content from Azure Blob Storage
    """

    def __init__(self, token):
        self._token = token

    def get_content(self, url):
        return requests.get(url).content
