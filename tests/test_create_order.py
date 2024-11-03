import pytest


@pytest.mark.asyncio
async def test_create_order(client):
    # Créer un client pour garantir que customer_id est valide
    response = await client.post("/customers/", json={
        "name": "Test Customer",
        "email": "test_customer@example.com",
        "address": "123 Test Street"
    })
    assert response.status_code == 201
    customer_id = response.json()["id"]

    # Créer une commande avec le client créé
    response = await client.post("/orders/", json={
        "customer_id": customer_id,
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
    assert response.status_code == 201
    data = response.json()
    assert data["customer_id"] == customer_id
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
