import requests


class APIClient:
    """A reusable client to make HTTP requests."""

    def __init__(self, base_url, port, headers=None):
        self.base_url = base_url
        self.port = port
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def get(self, endpoint, params=None, **kwargs):
        """Sends a GET request."""
        url = f"{self.base_url}:{self.port}{endpoint}"
        return self.session.get(url, params=params, **kwargs)

    def post(self, endpoint, data=None, json=None, **kwargs):
        """Sends a POST request."""
        url = f"{self.base_url}:{self.port}{endpoint}"
        return self.session.post(url, data=data, json=json, **kwargs)

    def put(self, endpoint, data=None, **kwargs):
        """Sends a PUT request."""
        url = f"{self.base_url}:{self.port}{endpoint}"
        return self.session.put(url, data=data, **kwargs)

    def delete(self, endpoint, **kwargs):
        """Sends a DELETE request."""
        url = f"{self.base_url}:{self.port}{endpoint}"
        return self.session.delete(url, **kwargs)
