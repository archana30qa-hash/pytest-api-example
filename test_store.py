from jsonschema import validate
import pytest
import schemas
import api_helpers
import random
from hamcrest import assert_that, contains_string, is_

@pytest.fixture
def new_order():
    # Unique test data using random ID
    pet_id = random.randint(1, 1000)
    pet_data = {
        "id": pet_id,
        "name": "ranger",
        "status": "available",
        "type": "dog"
    }

    pet_response = api_helpers.post_api_data("/pets", pet_data)
    assert pet_response.status_code == 201, f"Failed to create pet, got {pet_response.status_code}"

    order_data = {
        "pet_id": pet_id,
        "quantity": 1,
        "shipDate": "2025-08-06T00:00:00Z",
        "status": "placed",
        "complete": False
    }

    order_response = api_helpers.post_api_data("/store/order", order_data)
    assert order_response.status_code == 201, f"Failed to create order, got {order_response.status_code}"

    order_json = order_response.json()
    assert "id" in order_json, "Order response did not contain 'id'"

    return order_json  


def test_patch_order_by_id(new_order):
    # Testing PATCH endpoint
    order_id = new_order["id"]
    test_endpoint = f"/store/order/{order_id}"

    patch_data = {
        "status": "available"
    }

    response = api_helpers.patch_api_data(test_endpoint, patch_data)

    # Validate response code
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    response_data = response.json()

    #  Validate with 'Order' schema (optional)
    if hasattr(schemas, 'order'):
        validate(instance=response_data, schema=schemas.order)

    # Validate success message
    assert response_data.get("message") == "Order and pet status updated successfully", \
        f"Unexpected message: {response_data.get('message')}"
