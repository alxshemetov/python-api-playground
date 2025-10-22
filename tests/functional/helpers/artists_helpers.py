from requests import Response

from api_framework.models.artists_model import ArtistResponse


def assert_artist_data(response: Response, expected_user_id, expected_data):
    artist_response: ArtistResponse = ArtistResponse.model_validate_json(response.text)
    assert artist_response.user_id == expected_user_id
    assert artist_response.first_name == expected_data.first_name
    assert artist_response.last_name == expected_data.last_name
    assert artist_response.birth_year == int(expected_data.birth_year)
