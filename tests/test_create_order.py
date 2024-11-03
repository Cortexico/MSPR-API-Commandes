import pytest


@pytest.mark.asyncio
async def test_create_order(client):
    response = await client.post("/orders/", json={
        "customer_id": 1,
        "total_amount": 99.99,
        "status": "pending"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["customer_id"] == 1
    assert data["total_amount"] == 99.99
    assert data["status"] == "pending"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_order_with_invalid_data(client):
    response = await client.post("/orders/", json={
        "customer_id": "invalid_id",  # Invalid ID
        "total_amount": "invalid_amount",  # Invalid amount
        "status": "pending"
    })
    assert response.status_code == 422  # Validation error
