import http
import allure
from pytest_check import check
from assertpy import assert_that

from python_api_playground.models.artists_model import ArtistResponse, ArtistCreate
from python_api_playground.services.artists_service import ArtistsService


class ArtistSteps:
    def __init__(self, artists_service: ArtistsService):
        self.artists_service = artists_service

    @allure.step("Create a new artist")
    def create_artist(self, new_artist: ArtistCreate) -> int:
        create_response = self.artists_service.create_artist(new_artist)
        assert_that(create_response.status_code).is_equal_to(http.HTTPStatus.OK)
        user_id = create_response.json()
        return user_id
