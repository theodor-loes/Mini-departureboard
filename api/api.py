import requests


class Api:
    def __init__(self, url: str, query=None, headers=None):
        self.url = url
        self.query = query
        self.headers = headers

        if query:
            method = 'POST'
        else:
            method = 'GET'
        self.JSON = self.request(method=method)

    def request(self, method: str = 'GET'):
        if method.upper() == 'GET':
            response = requests.get(self.url, headers=self.headers)
        elif method.upper() == 'POST':
            response = requests.post(self.url, json={"query": self.query}, headers=self.headers)
        else:
            raise ValueError(f'{method} is an invalid method')

        return response.json()
