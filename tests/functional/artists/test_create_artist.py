from http import HTTPStatus

import pytest

from api_framework.models.artists_model import ArtistResponse, ArtistCreate
from tests.functional.helpers.artists_helpers import assert_artist_data
from tests.functional.helpers.common_helpers import assert_error_response
from tests.functional.test_data import artist_test_payloads as payloads


def test_create_artist(artists_service, create_new_artist):
    user_id, new_artist = create_new_artist

    all_artists_response = artists_service.get_all_artists()
    assert any(artist.user_id == user_id for artist in all_artists_response)

    artist_response: ArtistResponse = artists_service.get_artist_by_id(str(user_id))
    assert_artist_data(artist_response, user_id, new_artist)


@pytest.mark.parametrize("artist_payload", payloads.CREATE_ARTIST_EMPTY_FIELD_PAYLOADS)
def test_create_artist_with_empty_field(artists_service, artist_payload):
    invalid_artist = ArtistCreate(**artist_payload)

    error_response = artists_service.create_artist(invalid_artist)
    assert_error_response(error_response, HTTPStatus.BAD_REQUEST, "All fields must be non-empty strings")


@pytest.mark.parametrize("artist_payload", payloads.CREATE_ARTIST_MISSING_FIELD_PAYLOADS)
def test_create_artist_with_missing_field(artists_service, artist_payload):
    invalid_artist = ArtistCreate(**artist_payload)

    error_response = artists_service.create_artist(invalid_artist)
    assert_error_response(error_response, HTTPStatus.BAD_REQUEST, "Missing keys")


@pytest.mark.parametrize("artist_payload", payloads.CREATE_ARTIST_INVALID_DATA_TYPE_PAYLOADS)
def test_create_artist_with_invalid_data_type(artists_service, artist_payload):
    error_response = artists_service.client.post("/artists", json=artist_payload)
    assert_error_response(error_response, HTTPStatus.BAD_REQUEST, "All fields must be non-empty strings")


def test_create_artist_with_empty_payload(artists_service):
    invalid_artist = ArtistCreate()

    error_response = artists_service.create_artist(invalid_artist)
    assert_error_response(error_response, HTTPStatus.BAD_REQUEST, "Invalid JSON payload")
