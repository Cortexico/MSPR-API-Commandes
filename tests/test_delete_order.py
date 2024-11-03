import pytest


@pytest.mark.asyncio
async def test_delete_order(client):
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

    # Delete the order
    delete_response = await client.delete(f"/orders/{order_id}")
    assert delete_response.status_code == 204

    # Verify the order no longer exists
    fetch_response = await client.get(f"/orders/{order_id}")
    assert fetch_response.status_code == 404
