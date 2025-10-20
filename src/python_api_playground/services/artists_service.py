from typing import List

from python_api_playground.api_client import APIClient
from python_api_playground.models.artists_model import (
    ArtistCreate,
    ArtistResponse,
    ArtistUpdate,
    ArtistDeleteResponse
)


class ArtistsService:

    def __init__(self, client: APIClient):
        self.client = client
        self.endpoint = "/artists"

    def get_all_artists(self) -> List[ArtistResponse]:
        response = self.client.get(self.endpoint)
        return [ArtistResponse.model_validate(artist) for artist in response.json()]

    def get_artist_by_id(self, user_id: str) -> ArtistResponse:
        response = self.client.get(f"{self.endpoint}/{user_id}")
        if response.ok:
            return ArtistResponse.model_validate(response.json())
        else:
            return response

    def create_artist(self, new_artist: ArtistCreate):
        payload = new_artist.model_dump(exclude_none=True)
        response = self.client.post(self.endpoint, json=payload)
        return response

    def update_artist(self, updated_artist: ArtistUpdate):
        payload = updated_artist.model_dump()
        response = self.client.put(self.endpoint, json=payload)
        return response

    def delete_artist(self, user_id: str):
        response = self.client.delete(f"{self.endpoint}/{user_id}")
        return response
