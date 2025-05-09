import pytest


@pytest.mark.asyncio
async def test_get_order(client):
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

    # Get the order
    response = await client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["customer_id"] == 1
    assert data["total_amount"] == 99.99
    assert data["status"] == "pending"
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == "test_product"


@pytest.mark.asyncio
async def test_get_nonexistent_order(client):
    response = await client.get("/orders/9999")  # Assuming ID 9999 does not exist
    assert response.status_code == 404
