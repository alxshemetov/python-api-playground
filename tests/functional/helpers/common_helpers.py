def assert_error_response(error_response, expected_status_code, expected_message):
    assert error_response.status_code == expected_status_code
    response_json = error_response.json()
    assert "error" in response_json
    assert expected_message in response_json["error"]
