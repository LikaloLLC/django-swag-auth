import json

import requests


class BitbucketAPIClient:
    api_url: str = 'https://api.bitbucket.org/2.0/'

    def __init__(self, token):
        self._token = token

    def get_header(self):
        """
        Return the request header
        :return:
        """
        headers = {
            'Authorization': f'Bearer {self._token}'
        }
        return headers

    def get_content(self, repo_name, path_file, ref):
        """
        Returns the content of the given file
        :param repo_name:
        :param path_file:
        :return:
        """
        url = self.api_url + 'repositories/' + repo_name + f'/src/{ref}/' + path_file + '?ref=' + ref
        return json.loads(requests.get(url=url, headers=self.get_header()).content)['values']
