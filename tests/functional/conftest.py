import http

import pytest
from faker import Faker

from python_api_playground.models.artists_model import ArtistCreate
from python_api_playground.services.artists_service import ArtistsService

fake = Faker()


@pytest.fixture(scope="module")
def artists_service(api_client):
    return ArtistsService(api_client)


@pytest.fixture
def generate_artist_data() -> ArtistCreate:
    return ArtistCreate(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        birth_year=fake.year()
    )


@pytest.fixture
def create_new_artist(artists_service, generate_artist_data):
    new_artist = generate_artist_data
    create_response = artists_service.create_artist(new_artist)
    assert create_response.status_code == http.HTTPStatus.OK
    user_id = create_response.json()

    yield user_id, new_artist

    try:
        artists_service.delete_artist(str(user_id))
    except Exception:
        pass
