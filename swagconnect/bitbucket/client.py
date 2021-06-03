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

    def get_bitbucket_content(self, repo_name, path_file):
        """
        Returns the content of the given file
        :param repo_name:
        :param path_file:
        :return:
        """
        url = self.api_url + 'repositories/' + repo_name + '/src/'
        repo_content = requests.get(url=url, headers=self.get_header())
        data = json.loads(repo_content.content.decode('utf-8'))
        hash = data['values'][0]['commit']['hash']
        url = url + hash + '/' + path_file
        return requests.get(url=url, headers=self.get_header()).content
