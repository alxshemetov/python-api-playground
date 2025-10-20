from http import HTTPStatus

import pytest

from python_api_playground.models.artists_model import ArtistUpdate, ArtistResponse
from tests.functional.conftest import fake
from tests.functional.helpers.artists_helpers import assert_artist_data
from tests.functional.helpers.common_helpers import assert_error_response
from tests.functional.test_data import artist_test_payloads as payloads


def test_update_artist(artists_service, create_new_artist):
    user_id, new_artist = create_new_artist

    update_data = ArtistUpdate(
        user_id=str(user_id),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        birth_year=fake.year()
    )

    update_response = artists_service.update_artist(update_data)
    assert update_response.status_code == HTTPStatus.OK
    assert update_response.json() == True

    updated_artist_response: ArtistResponse = artists_service.get_artist_by_id(str(user_id))
    assert_artist_data(updated_artist_response, user_id, update_data)


@pytest.mark.parametrize("update_payload", payloads.UPDATE_ARTIST_EMPTY_FIELD_PAYLOADS)
def test_update_artist_with_empty_field(artists_service, create_new_artist, update_payload):
    user_id, new_artist = create_new_artist

    invalid_update = ArtistUpdate(**update_payload)

    error_response = artists_service.update_artist(invalid_update)
    assert_error_response(error_response, HTTPStatus.BAD_REQUEST, "All fields must be non-empty strings")


@pytest.mark.parametrize("update_payload", payloads.UPDATE_ARTIST_MISSING_FIELD_PAYLOADS)
def test_update_artist_with_missing_field(artists_service, create_new_artist, update_payload):
    user_id, new_artist = create_new_artist

    if "user_id" in update_payload:
        update_payload["user_id"] = str(user_id)

    invalid_update = ArtistUpdate(**update_payload)

    error_response = artists_service.update_artist(invalid_update)
    assert_error_response(error_response, HTTPStatus.BAD_REQUEST, "Missing keys")
