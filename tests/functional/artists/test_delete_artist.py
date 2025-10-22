from http import HTTPStatus

from api_framework.models.artists_model import ArtistResponse


def test_delete_artist(artists_service, create_new_artist):
    user_id = create_new_artist

    delete_response = artists_service.delete_artist(str(user_id))
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json() is True

    all_artists_response = artists_service.get_all_artists()
    all_artists = [ArtistResponse.model_validate(artist) for artist in all_artists_response.json()]
    assert user_id not in [artist.user_id for artist in all_artists]


def test_delete_artist_with_invalid_id(artists_service):
    error_response = artists_service.delete_artist("non-existent-id")
    assert error_response.status_code == HTTPStatus.NOT_FOUND
