import pytest


@pytest.mark.asyncio
async def test_create_order(client):
    # Utiliser le customer_id créé par défaut dans la base de données de test (ID=1 par exemple)
    response = await client.post("/orders/", json={
        "customer_id": 1,  # Assure-toi que cet ID est correct selon ce que tu as en base
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
