import pytest


@pytest.mark.asyncio
async def test_update_order(client):
    # Create an order with an item
    create_response = await client.post("/orders/", json={
        "customer_id": 1,
        "total_amount": 99.99,
        "status": "pending",
        "items": [
            {
                "product_id": "test_product",
                "quantity": 1,
                "price": 99.99
            }
        ]
    })
    assert create_response.status_code == 201
    order_id = create_response.json()["id"]

    # Update the order
    update_response = await client.put(f"/orders/{order_id}", json={
        "status": "completed"
    })
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["status"] == "completed"
