import pytest

CREATE_ARTIST_EMPTY_FIELD_PAYLOADS = [
    pytest.param({"first_name": "", "last_name": "Monet", "birth_year": "1840"}, id="empty_first_name"),
    pytest.param({"first_name": "Claude", "last_name": "", "birth_year": "1840"}, id="empty_last_name"),
    pytest.param({"first_name": "Claude", "last_name": "Monet", "birth_year": ""}, id="empty_birth_year"),
]

CREATE_ARTIST_MISSING_FIELD_PAYLOADS = [
    pytest.param({"last_name": "Monet", "birth_year": "1840"}, id="missing_first_name"),
    pytest.param({"first_name": "Claude", "birth_year": "1840"}, id="missing_last_name"),
    pytest.param({"first_name": "Claude", "last_name": "Monet"}, id="missing_birth_year"),
]

CREATE_ARTIST_INVALID_DATA_TYPE_PAYLOADS = [
    pytest.param({"first_name": 12345, "last_name": "Monet", "birth_year": "1840"}, id="invalid_first_name_type"),
    pytest.param({"first_name": "Claude", "last_name": True, "birth_year": "1840"}, id="invalid_last_name_type"),
    pytest.param({"first_name": "Claude", "last_name": "Monet", "birth_year": []}, id="invalid_birth_year_type"),
]

UPDATE_ARTIST_EMPTY_FIELD_PAYLOADS = [
    pytest.param({"user_id": "", "first_name": "Claude", "last_name": "Monet", "birth_year": "1840"}, id="empty_user_id"),
    pytest.param({"user_id": "1", "first_name": "", "last_name": "Monet", "birth_year": "1840"}, id="empty_first_name"),
    pytest.param({"user_id": "1", "first_name": "Claude", "last_name": "", "birth_year": "1840"}, id="empty_last_name"),
    pytest.param({"user_id": "1", "first_name": "Claude", "last_name": "Monet", "birth_year": ""}, id="empty_birth_year"),
]

UPDATE_ARTIST_MISSING_FIELD_PAYLOADS = [
    pytest.param({"first_name": "Claude", "last_name": "Monet", "birth_year": "1840"}, id="missing_user_id"),
    pytest.param({"user_id": "", "last_name": "Monet", "birth_year": "1840"}, id="missing_first_name"),
    pytest.param({"user_id": "", "first_name": "Claude", "birth_year": "1840"}, id="missing_last_name"),
    pytest.param({"user_id": "", "first_name": "Claude", "last_name": "Monet"}, id="missing_birth_year"),
]
