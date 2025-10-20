import http

import allure
import pytest

from python_api_playground.models.artists_model import ArtistResponse, ArtistUpdate, ArtistCreate
from tests.functional.conftest import fake
from tests.functional.helpers.common_helpers import assert_error_response
from tests.functional.helpers.artists_helpers import assert_artist_data
from tests.functional.test_data import artist_test_payloads as payloads


# --- Positive Tests ---

@allure.title("Create Artist")
def test_create_artist(artists_service, artist_steps, generate_artist_data):
    # Step 1: Create a new artist
    new_artist = generate_artist_data
    user_id = artist_steps.create_artist(new_artist)

    # Step 2: Verify the new artist appears in the full list of artists.
    all_artists_response = artists_service.get_all_artists()
    assert any(artist.user_id == user_id for artist in all_artists_response)

    # Step 3: Verify the details of the newly created artist by fetching it directly.
    artist_response: ArtistResponse = artists_service.get_artist_by_id(str(user_id))
    assert_artist_data(artist_response, user_id, new_artist)


@allure.title("Get All Artists")
def test_get_all_artists(artists_service, artist_steps, generate_artist_data):
    # Step 1: Create a new artist
    new_artist = generate_artist_data
    user_id = artist_steps.create_artist(new_artist)

    # Step 2: Retrieve the full list of artists from the API.
    all_artists = artists_service.get_all_artists()

    # Step 3: Perform high-level validation on the list.
    assert isinstance(all_artists, list)
    assert len(all_artists) > 0, "The artists list should not be empty."

    # Step 4: Find our artist and verify its data is correctly represented in the list.
    found_artist = next((artist for artist in all_artists if artist.user_id == user_id), None)

    assert found_artist is not None, "The created artist was not found in the GET /artists list."
    assert isinstance(found_artist, ArtistResponse)
    assert found_artist.first_name == new_artist.first_name
    assert found_artist.last_name == new_artist.last_name
    assert str(found_artist.birth_year) == new_artist.birth_year


@allure.title("Get Artist By ID")
def test_get_artist_by_id(artists_service, artist_steps, generate_artist_data):
    # Step 1: Create a new artist
    new_artist = generate_artist_data
    user_id = artist_steps.create_artist(new_artist)

    # Step 2: Verify the details of the newly created artist by fetching it directly.
    artist_response: ArtistResponse = artists_service.get_artist_by_id(str(user_id))
    assert_artist_data(artist_response, user_id, new_artist)


@allure.title("Update Artist")
def test_update_artist(artists_service, artist_steps, generate_artist_data):
    # Step 1: Create a new artist
    new_artist = generate_artist_data
    user_id = artist_steps.create_artist(new_artist)

    # Step 2: Define the updated artist data.
    update_data = ArtistUpdate(
        user_id=str(user_id),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        birth_year=fake.year()
    )

    # Step 3: Update the artist.
    update_response = artists_service.update_artist(update_data)
    assert update_response.status_code == http.HTTPStatus.OK
    assert update_response.json() == True

    # Step 4: Verify the artist's details have been updated.
    updated_artist_response: ArtistResponse = artists_service.get_artist_by_id(str(user_id))
    assert_artist_data(updated_artist_response, user_id, update_data)


@allure.title("Delete Artist")
def test_delete_artist(artists_service, artist_steps, generate_artist_data):
    # Step 1: Create a new artist
    new_artist = generate_artist_data
    user_id = artist_steps.create_artist(new_artist)

    # Step 2: Delete the artist.
    delete_response = artists_service.delete_artist(str(user_id))
    assert delete_response.status_code == http.HTTPStatus.OK
    assert delete_response.json() is True

    # Step 3: Verify the artist is no longer in the full list.
    all_artists_response = artists_service.get_all_artists()
    assert user_id not in [artist.user_id for artist in all_artists_response]


# --- Negative Tests ---

@allure.title("Create artist with empty field returns 400")
@pytest.mark.parametrize("artist_payload", payloads.CREATE_ARTIST_EMPTY_FIELD_PAYLOADS)
def test_create_artist_with_empty_field(artists_service, artist_payload):
    # Step 1: Create an artist model instance from a payload with an empty field.
    invalid_artist = ArtistCreate(**artist_payload)

    # Step 2: Attempt to create the artist.
    error_response = artists_service.create_artist(invalid_artist)

    # Step 3: Verify the error response
    assert_error_response(error_response, http.HTTPStatus.BAD_REQUEST, "All fields must be non-empty strings")


@allure.title("Create artist with missing required field returns 400")
@pytest.mark.parametrize("artist_payload", payloads.CREATE_ARTIST_MISSING_FIELD_PAYLOADS)
def test_create_artist_with_missing_field(artists_service, artist_payload):
    # Step 1: Create an artist model instance from a payload with a missing required field.
    invalid_artist = ArtistCreate(**artist_payload)

    # Step 2: Attempt to create the artist. The service will now exclude the missing (None) fields.
    error_response = artists_service.create_artist(invalid_artist)

    # Step 3: Verify the error response
    assert_error_response(error_response, http.HTTPStatus.BAD_REQUEST, "Missing keys")


@allure.title("Create artist with invalid data type returns 400")
@pytest.mark.parametrize("artist_payload", payloads.CREATE_ARTIST_INVALID_DATA_TYPE_PAYLOADS)
def test_create_artist_with_invalid_data_type(artists_service, artist_payload):
    # Step 1: Attempt to create an artist using a payload with an invalid data type.
    error_response = artists_service.client.post("/artists", json=artist_payload)

    # Step 2: Verify the error response
    assert_error_response(error_response, http.HTTPStatus.BAD_REQUEST, "All fields must be non-empty strings")


@allure.title("Create artist with empty payload returns 400")
def test_create_artist_with_empty_payload(artists_service):
    # Step 1: Create an artist model instance from a payload with an empty field.
    invalid_artist = ArtistCreate()

    # Step 2: Attempt to create the artist.
    error_response = artists_service.create_artist(invalid_artist)

    # Step 3: Verify the error response
    assert_error_response(error_response, http.HTTPStatus.BAD_REQUEST, "Invalid JSON payload")


@allure.title("Get non-existent artist returns 404")
def test_get_non_existent_artist(artists_service):
    # Step 1: Attempt to fetch an artist that doesn't exist.
    error_response = artists_service.get_artist_by_id("non-existent-id")

    # Step 2: Verify the error response is returned.
    assert error_response.status_code == http.HTTPStatus.NOT_FOUND


@allure.title("Get Artist with Empty ID")
def test_get_artist_with_empty_id(artists_service):
    # Step 1: Attempt to fetch an artist with an empty ID.
    error_response = artists_service.get_artist_by_id("")

    # Step 2: Verify the error response is returned.
    assert error_response.status_code == http.HTTPStatus.NOT_FOUND


@allure.title("Update artist artist with empty field returns 400")
@pytest.mark.parametrize("update_payload", payloads.UPDATE_ARTIST_EMPTY_FIELD_PAYLOADS)
def test_update_artist_with_empty_field(artists_service, artist_steps, generate_artist_data, update_payload):
    # Step 1: Create a new artist to update
    new_artist = generate_artist_data
    artist_steps.create_artist(new_artist)

    # Step 2: Create an ArtistUpdate instance with missing
    invalid_update = ArtistUpdate(**update_payload)

    # Step 3: Attempt to update the artist
    error_response = artists_service.update_artist(invalid_update)

    # Step 4: Verify the error response
    assert_error_response(error_response, http.HTTPStatus.BAD_REQUEST, "All fields must be non-empty strings")


@allure.title("Update artist with missing required field returns 400")
@pytest.mark.parametrize("update_payload", payloads.UPDATE_ARTIST_MISSING_FIELD_PAYLOADS)
def test_update_artist_with_missing_field(artists_service, artist_steps, generate_artist_data, update_payload):
    # Step 1: Create a new artist to update
    new_artist = generate_artist_data
    user_id = artist_steps.create_artist(new_artist)

    # Step 2: If user_id is in the payload, replace it with the actual user_id
    if "user_id" in update_payload:
        update_payload["user_id"] = str(user_id)

    # Step 3: Create an ArtistUpdate instance with missing
    invalid_update = ArtistUpdate(**update_payload)

    # Step 4: Attempt to update the artist
    error_response = artists_service.update_artist(invalid_update)

    # Step 5: Verify the error response
    assert_error_response(error_response, http.HTTPStatus.BAD_REQUEST, "Missing keys")


@allure.title("Delete non-existent artist returns 404")
def test_delete_artist_with_invalid_id(artists_service, artist_steps):
    # Step 1: Attempt to delete an artist that doesn't exist.
    error_response = artists_service.delete_artist("non-existent-id")

    # Step 2: Verify the error response is returned.
    assert error_response.status_code == http.HTTPStatus.NOT_FOUND
