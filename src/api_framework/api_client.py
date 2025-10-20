import requests
import allure


class APIClient:
    def __init__(self, base_url, port, headers=None):
        self.base_url = base_url
        self.port = port
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def get(self, endpoint, params=None, **kwargs):
        url = f"{self.base_url}:{self.port}{endpoint}"
        with allure.step(f"Send GET request: {url}"):
            return self.session.get(url, params=params, **kwargs)

    def post(self, endpoint, data=None, json=None, **kwargs):
        url = f"{self.base_url}:{self.port}{endpoint}"
        with allure.step(f"Send POST request: {url}"):
            return self.session.post(url, data=data, json=json, **kwargs)

    def put(self, endpoint, data=None, **kwargs):
        url = f"{self.base_url}:{self.port}{endpoint}"
        with allure.step(f"Send PUT request: {url}"):
            return self.session.put(url, data=data, **kwargs)

    def delete(self, endpoint, **kwargs):
        url = f"{self.base_url}:{self.port}{endpoint}"
        with allure.step(f"Send DELETE request: {url}"):
            return self.session.delete(url, **kwargs)
