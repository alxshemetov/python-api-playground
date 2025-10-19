import pytest
from faker import Faker

from python_api_playground.models.artists_model import ArtistCreate

from python_api_playground.services.artists_service import ArtistsService

# Initialize the Faker instance
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
