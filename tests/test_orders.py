import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_create_order(client):
    with patch('app.crud.publish_order_created', new_callable=AsyncMock):
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
async def test_get_order(client):
    with patch('app.crud.publish_order_created', new_callable=AsyncMock):
        create_response = await client.post("/orders/", json={
            "customer_id": 1,
            "total_amount": 99.99,
            "status": "pending"
        })
    assert create_response.status_code == 201
    order_id = create_response.json()["id"]

    response = await client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id

@pytest.mark.asyncio
async def test_update_order(client):
    with patch('app.crud.publish_order_created', new_callable=AsyncMock):
        create_response = await client.post("/orders/", json={
            "customer_id": 1,
            "total_amount": 99.99,
            "status": "pending"
        })
    assert create_response.status_code == 201
    order_id = create_response.json()["id"]

    update_response = await client.put(f"/orders/{order_id}", json={
        "status": "completed"
    })
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["status"] == "completed"

@pytest.mark.asyncio
async def test_delete_order(client):
    with patch('app.crud.publish_order_created', new_callable=AsyncMock):
        create_response = await client.post("/orders/", json={
            "customer_id": 1,
            "total_amount": 99.99,
            "status": "pending"
        })
    assert create_response.status_code == 201
    order_id = create_response.json()["id"]

    delete_response = await client.delete(f"/orders/{order_id}")
    assert delete_response.status_code == 204

    fetch_response = await client.get(f"/orders/{order_id}")
    assert fetch_response.status_code == 404

@pytest.mark.asyncio
async def test_create_order_with_invalid_data(client):
    response = await client.post("/orders/", json={
        "customer_id": "invalid_id",
        "total_amount": "invalid_amount",
        "status": "pending"
    })
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_get_nonexistent_order(client):
    response = await client.get("/orders/9999")
    assert response.status_code == 404
