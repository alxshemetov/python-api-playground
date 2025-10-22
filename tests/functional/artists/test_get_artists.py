from api_framework.models.artists_model import ArtistResponse


def test_get_artists(artists_service, create_new_artist):
    user_id, new_artist = create_new_artist

    all_artists_response = artists_service.get_all_artists()
    all_artists_response: list[ArtistResponse] = [ArtistResponse.model_validate(artist) for artist in all_artists_response.json()]
    assert isinstance(all_artists_response, list)
    assert len(all_artists_response) > 0, "The artists list should not be empty."

    found_artist = next((artist for artist in all_artists_response if artist.user_id == user_id), None)
    assert found_artist is not None, "The created artist was not found in the GET /artists list."
    assert isinstance(found_artist, ArtistResponse)
    assert found_artist.first_name == new_artist.first_name
    assert found_artist.last_name == new_artist.last_name
    assert str(found_artist.birth_year) == new_artist.birth_year
