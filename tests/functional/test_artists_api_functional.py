import http
import allure
from assertpy import assert_that

from python_api_playground.models.artists_model import ArtistResponse, ArtistCreate
from tests.functional.steps.artists_steps import ArtistSteps


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
    assert user_id == artist_response.user_id
    assert artist_response.first_name == new_artist.first_name
    assert artist_response.last_name == new_artist.last_name
    assert artist_response.birth_year == new_artist.birth_year


@allure.title("Get All Artists")
def test_get_all_artists(artists_service, artist_steps, generate_artist_data):
    # Step 1: Ensure the database isn't empty by creating an artist.
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
    # Step 1: Ensure the database isn't empty by creating an artist.
    new_artist = generate_artist_data
    user_id = artist_steps.create_artist(new_artist)

    # Step 2: Verify the details of the newly created artist by fetching it directly.
    artist_response: ArtistResponse = artists_service.get_artist_by_id(str(user_id))
    assert user_id == artist_response.user_id
    assert artist_response.first_name == new_artist.first_name
    assert artist_response.last_name == new_artist.last_name
    assert artist_response.birth_year == new_artist.birth_year
