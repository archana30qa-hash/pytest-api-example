from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_


def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)


@pytest.mark.parametrize("status", ["available", "pending", "sold"]) #adjusted and added more statuses
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)
    #validates the response code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    pets = response.json()
    assert isinstance(pets, list), "Response is not a list of pets"

    for pet in pets:
        assert pet.get("status") == status, f"Expected status {status}, got {pet.get('status')}"
        validate(instance=pet, schema=schemas.pet)

#checks for a 404 response
@pytest.mark.parametrize("invalid_id", [-1, 999999, "invalid_id"])
def test_get_by_id_404(invalid_id): 
    test_endpoint = f"/pets/{invalid_id}"

    response = api_helpers.get_api_data(test_endpoint)
    assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"

    if response.headers.get("Content-Type", "").startswith("application/json"):
        try:
            error_data = response.json()
            if error_data:
                assert "message" in error_data, "Error response should contain 'message'"
                assert_that(error_data["message"], contains_string("not found"))
        except ValueError:
            pass
