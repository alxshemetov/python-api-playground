from requests import Response

from api_framework.api_client import APIClient
from api_framework.models.artists_model import (ArtistCreate, ArtistUpdate)


class ArtistsService:

    def __init__(self, client: APIClient):
        self.client = client
        self.endpoint = "/artists"

    def get_all_artists(self) -> Response:
        return self.client.get(self.endpoint)

    def get_artist_by_id(self, user_id: str) -> Response:
        return self.client.get(f"{self.endpoint}/{user_id}")

    def create_artist(self, new_artist: ArtistCreate) -> Response:
        return self.client.post(self.endpoint, json=new_artist.model_dump())

    def create_artist_raw(self, new_artist: dict) -> Response:
        return self.client.post(self.endpoint, json=new_artist)

    def update_artist(self, updated_artist: ArtistUpdate) -> Response:
        return self.client.put(self.endpoint, json=updated_artist.model_dump())

    def update_artist_raw(self, updated_artist: dict) -> Response:
        return self.client.put(self.endpoint, json=updated_artist)

    def delete_artist(self, user_id: str) -> Response:
        return self.client.delete(f"{self.endpoint}/{user_id}")
