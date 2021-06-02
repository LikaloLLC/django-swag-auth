import json

import requests


class BaseBitbucket:
    def __init__(self, token):
        self._token = token
        self._api_url = 'https://api.bitbucket.org/2.0/'

    def get_header(self):
        headers = {
            'Authorization': f'Bearer {self._token}'
        }
        return headers

    def get_bitbucket_content(self, repo_name, path_file):
        url = self._api_url + 'repositories/' + repo_name + '/src/'
        repo_content = requests.get(url=url, headers=self.get_header())
        data = json.loads(repo_content.content.decode('utf-8'))
        hash = data['values'][0]['commit']['hash']
        url = url + hash + '/' + path_file
        answer = requests.get(url=url, headers=self.get_header()).content
        return answer
