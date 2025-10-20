import os

import pytest
from dotenv import load_dotenv

from python_api_playground.api_client import APIClient

pytest.register_assert_rewrite("tests.functional.helpers", "tests.functional.steps")

# Load environment variables once for all tests
load_dotenv()


@pytest.fixture(scope="session")
def api_client():
    base_url: str | None = os.getenv('API_BASE_URI')
    port: str | None = os.getenv('API_PORT')
    return APIClient(base_url, port)
