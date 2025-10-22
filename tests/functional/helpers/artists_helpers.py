from api_framework.models.artists_model import ArtistResponse


def assert_artist_data(artist_response, expected_user_id, expected_data):
    artist_response: ArtistResponse = ArtistResponse.model_validate(artist_response.json())
    assert artist_response.user_id == expected_user_id, f"Expected user_id: {expected_user_id}, but got: {artist_response.user_id}"
    assert artist_response.first_name == expected_data.first_name, f"Expected first_name: {expected_data.first_name}, but got: {artist_response.first_name}"
    assert artist_response.last_name == expected_data.last_name, f"Expected last_name: {expected_data.last_name}, but got: {artist_response.last_name}"
    assert artist_response.birth_year == int(expected_data.birth_year), f"Expected birth_year: {expected_data.birth_year}, but got: {artist_response.birth_year}"
