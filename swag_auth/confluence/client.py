import requests


class Client:
    def __init__(self, email, token, domain):
        self.domain = domain
        self.token = token
        self.email = email
        self.headers = {'Accept': 'application/json'}
        self.auth = (email, self.token)
        self.base_url = f'https://{self.domain}.atlassian.net/wiki/rest/api/content'

    def _request(self, endpoint: str):
        if not endpoint[:1] == '/':  # adding slash pre endpoint if you forgot adding this
            endpoint = '/' + endpoint

        url = self.base_url + endpoint

        response = requests.get(url, auth=self.auth, headers=self.headers)

        return response

    def get_page_html(self, page_id):
        response = self._request(endpoint=f'{page_id}?expand=body.storage')
        return response.json()['body']['storage']['value']

    def list_pages_ids(self):
        response = self._request('/').json()  # request to the base url
        return [page['id'] for page in response.get("results", []) if 'id' in page]
