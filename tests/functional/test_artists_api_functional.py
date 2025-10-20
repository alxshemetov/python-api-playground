import allure
import pytest

from http import HTTPStatus
from python_api_playground.models.artists_model import ArtistResponse, ArtistUpdate, ArtistCreate
from tests.functional.conftest import fake
from tests.functional.helpers.common_helpers import assert_error_response
from tests.functional.helpers.artists_helpers import assert_artist_data
from tests.functional.test_data import artist_test_payloads as payloads


@allure.title("Create Artist")
def test_create_artist(artists_service, artist_steps, generate_artist_data):
    new_artist = generate_artist_data
    user_id = artist_steps.create_artist(new_artist)

    all_artists_response = artists_service.get_all_artists()
    assert any(artist.user_id == user_id for artist in all_artists_response)

    artist_response: ArtistResponse = artists_service.get_artist_by_id(str(user_id))
    assert_artist_data(artist_response, user_id, new_artist)


@allure.title("Get All Artists")
def test_get_all_artists(artists_service, artist_steps, generate_artist_data):
    new_artist = generate_artist_data
    user_id = artist_steps.create_artist(new_artist)

    all_artists = artists_service.get_all_artists()

    assert isinstance(all_artists, list)
    assert len(all_artists) > 0, "The artists list should not be empty."

    found_artist = next((artist for artist in all_artists if artist.user_id == user_id), None)

    assert found_artist is not None, "The created artist was not found in the GET /artists list."
    assert isinstance(found_artist, ArtistResponse)
    assert found_artist.first_name == new_artist.first_name
    assert found_artist.last_name == new_artist.last_name
    assert str(found_artist.birth_year) == new_artist.birth_year


@allure.title("Get Artist By ID")
def test_get_artist_by_id(artists_service, artist_steps, generate_artist_data):
    new_artist = generate_artist_data
    user_id = artist_steps.create_artist(new_artist)

    artist_response: ArtistResponse = artists_service.get_artist_by_id(str(user_id))
    assert_artist_data(artist_response, user_id, new_artist)


@allure.title("Update Artist")
def test_update_artist(artists_service, artist_steps, generate_artist_data):
    new_artist = generate_artist_data
    user_id = artist_steps.create_artist(new_artist)

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


@allure.title("Delete Artist")
def test_delete_artist(artists_service, artist_steps, generate_artist_data):
    new_artist = generate_artist_data
    user_id = artist_steps.create_artist(new_artist)

    delete_response = artists_service.delete_artist(str(user_id))
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json() is True

    all_artists_response = artists_service.get_all_artists()
    assert user_id not in [artist.user_id for artist in all_artists_response]


@allure.title("Create artist with empty field returns 400")
@pytest.mark.parametrize("artist_payload", payloads.CREATE_ARTIST_EMPTY_FIELD_PAYLOADS)
def test_create_artist_with_empty_field(artists_service, artist_payload):
    invalid_artist = ArtistCreate(**artist_payload)

    error_response = artists_service.create_artist(invalid_artist)

    assert_error_response(error_response, HTTPStatus.BAD_REQUEST, "All fields must be non-empty strings")


@allure.title("Create artist with missing required field returns 400")
@pytest.mark.parametrize("artist_payload", payloads.CREATE_ARTIST_MISSING_FIELD_PAYLOADS)
def test_create_artist_with_missing_field(artists_service, artist_payload):
    invalid_artist = ArtistCreate(**artist_payload)

    error_response = artists_service.create_artist(invalid_artist)

    assert_error_response(error_response, HTTPStatus.BAD_REQUEST, "Missing keys")


@allure.title("Create artist with invalid data type returns 400")
@pytest.mark.parametrize("artist_payload", payloads.CREATE_ARTIST_INVALID_DATA_TYPE_PAYLOADS)
def test_create_artist_with_invalid_data_type(artists_service, artist_payload):
    error_response = artists_service.client.post("/artists", json=artist_payload)

    assert_error_response(error_response, HTTPStatus.BAD_REQUEST, "All fields must be non-empty strings")


@allure.title("Create artist with empty payload returns 400")
def test_create_artist_with_empty_payload(artists_service):
    invalid_artist = ArtistCreate()

    error_response = artists_service.create_artist(invalid_artist)

    assert_error_response(error_response, HTTPStatus.BAD_REQUEST, "Invalid JSON payload")


@allure.title("Get non-existent artist returns 404")
def test_get_non_existent_artist(artists_service):
    error_response = artists_service.get_artist_by_id("non-existent-id")

    assert error_response.status_code == HTTPStatus.NOT_FOUND


@allure.title("Get Artist with Empty ID")
def test_get_artist_with_empty_id(artists_service):
    error_response = artists_service.get_artist_by_id("")

    assert error_response.status_code == HTTPStatus.NOT_FOUND


@allure.title("Update artist artist with empty field returns 400")
@pytest.mark.parametrize("update_payload", payloads.UPDATE_ARTIST_EMPTY_FIELD_PAYLOADS)
def test_update_artist_with_empty_field(artists_service, artist_steps, generate_artist_data, update_payload):
    new_artist = generate_artist_data
    artist_steps.create_artist(new_artist)

    invalid_update = ArtistUpdate(**update_payload)

    error_response = artists_service.update_artist(invalid_update)

    assert_error_response(error_response, HTTPStatus.BAD_REQUEST, "All fields must be non-empty strings")


@allure.title("Update artist with missing required field returns 400")
@pytest.mark.parametrize("update_payload", payloads.UPDATE_ARTIST_MISSING_FIELD_PAYLOADS)
def test_update_artist_with_missing_field(artists_service, artist_steps, generate_artist_data, update_payload):
    new_artist = generate_artist_data
    user_id = artist_steps.create_artist(new_artist)

    if "user_id" in update_payload:
        update_payload["user_id"] = str(user_id)

    invalid_update = ArtistUpdate(**update_payload)

    error_response = artists_service.update_artist(invalid_update)

    assert_error_response(error_response, HTTPStatus.BAD_REQUEST, "Missing keys")


@allure.title("Delete non-existent artist returns 404")
def test_delete_artist_with_invalid_id(artists_service, artist_steps):
    error_response = artists_service.delete_artist("non-existent-id")

    assert error_response.status_code == HTTPStatus.NOT_FOUND
