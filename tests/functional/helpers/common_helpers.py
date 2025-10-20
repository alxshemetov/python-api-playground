def assert_error_response(response, expected_status_code, expected_message):
    assert response.status_code == expected_status_code
    response_json = response.json()
    assert "error" in response_json
    assert expected_message in response_json["error"]
