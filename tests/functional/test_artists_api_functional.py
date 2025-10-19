import http
import allure

from python_api_playground.models.artists_model import ArtistResponse


@allure.title("Create Artist")
def test_create_artist(artists_service, generate_artist_data):
    # Step 1: Create a new artist and verify the request was successful.
    new_artist = generate_artist_data
    create_response = artists_service.create_artist(new_artist)
    assert create_response.status_code == http.HTTPStatus.OK

    # Step 2: Verify the new artist appears in the full list of artists.
    user_id = create_response.json()
    all_artists_response = artists_service.get_all_artists()
    assert any(artist.user_id == user_id for artist in all_artists_response)

    # Step 3: Verify the details of the newly created artist by fetching it directly.
    artist_response: ArtistResponse = artists_service.get_artist_by_id(str(user_id))
    assert user_id == artist_response.user_id
    assert artist_response.first_name == new_artist.first_name
    assert artist_response.last_name == new_artist.last_name
    assert artist_response.birth_year == new_artist.birth_year
