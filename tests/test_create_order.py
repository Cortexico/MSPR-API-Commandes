import pytest


@pytest.mark.asyncio
async def test_create_order(client):
    # Utiliser le customer_id et le product_id créés par défaut dans la base de données de test
    response = await client.post("/orders/", json={
        "customer_id": 1,  # Assure-toi que cet ID est correct
        "total_amount": 99.99,
        "status": "pending",
        "items": [
            {
                "product_id": "test_product",  # Utilisation de l'ID du produit par défaut
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
