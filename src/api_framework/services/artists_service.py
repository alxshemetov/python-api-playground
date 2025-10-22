from typing import List, Union

from requests import Response

from api_framework.api_client import APIClient
from api_framework.models.artists_model import (
    ArtistCreate,
    ArtistResponse,
    ArtistUpdate
)


class ArtistsService:

    def __init__(self, client: APIClient):
        self.client = client
        self.endpoint = "/artists"

    def get_all_artists(self) -> List[ArtistResponse]:
        response = self.client.get(self.endpoint)
        return [ArtistResponse.model_validate(artist) for artist in response.json()]

    def get_artist_by_id(self, user_id: str) -> Response:
        return self.client.get(f"{self.endpoint}/{user_id}")

    def create_artist(self, new_artist: ArtistCreate) -> Response:
        payload = new_artist.model_dump(exclude_none=True)
        return self.client.post(self.endpoint, json=payload)

    def create_artist_raw(self, payload: dict) -> Response:
        return self.client.post(self.endpoint, json=payload)

    def update_artist(self, updated_artist: ArtistUpdate) -> Response:
        payload = updated_artist.model_dump(exclude_none=True)
        return self.client.put(self.endpoint, json=payload)

    def delete_artist(self, user_id: str) -> Response:
        return self.client.delete(f"{self.endpoint}/{user_id}")
