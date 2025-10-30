import os
import pytest

from dotenv import load_dotenv
from api_framework.api_client import APIClient

pytest.register_assert_rewrite("tests.functional.helpers", "tests.functional.steps")


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="session")
def api_client():
    base_url: str | None = os.getenv('API_BASE_URI')
    port: str | None = os.getenv('API_PORT')

    if not base_url:
        pytest.fail("API_BASE_URI environment variable is not set")
    if not port:
        pytest.fail("API_PORT environment variable is not set")

    client = APIClient(base_url, port)

    yield client

    client.session.close()
