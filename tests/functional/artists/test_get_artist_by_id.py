from http import HTTPStatus

from api_framework.models.artists_model import ArtistResponse
from tests.functional.helpers.artists_helpers import assert_artist_data


def test_get_artist_by_id(artists_service, create_new_artist):
    user_id, new_artist = create_new_artist

    artist_response: ArtistResponse = artists_service.get_artist_by_id(str(user_id))
    assert_artist_data(artist_response, user_id, new_artist)


def test_get_artist_with_non_existent_id(artists_service):
    error_response = artists_service.get_artist_by_id("non-existent-id")
    assert error_response.status_code == HTTPStatus.NOT_FOUND


def test_get_artist_with_empty_id(artists_service):
    error_response = artists_service.get_artist_by_id("")
    assert error_response.status_code == HTTPStatus.NOT_FOUND
