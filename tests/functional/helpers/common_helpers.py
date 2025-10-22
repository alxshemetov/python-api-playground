from requests import Response

from src.api_framework.models.artists_model import ErrorResponse


def assert_error_response(error_response: Response, expected_status_code, expected_message):
    assert error_response.status_code == expected_status_code
    error_model = ErrorResponse.model_validate_json(error_response.text)
    assert expected_message in error_model.error
