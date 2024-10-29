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
async def test_get_order(client):
    # Créer une commande pour le test
    create_response = await client.post("/orders/", json={
        "customer_id": 1,
        "total_amount": 99.99,
        "status": "pending"
    })
    assert create_response.status_code == 201
    order_id = create_response.json()["id"]

    # Récupérer la commande créée
    response = await client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["customer_id"] == 1
    assert data["total_amount"] == 99.99
    assert data["status"] == "pending"

@pytest.mark.asyncio
async def test_update_order(client):
    # Créer une commande pour le test
    create_response = await client.post("/orders/", json={
        "customer_id": 1,
        "total_amount": 99.99,
        "status": "pending"
    })
    assert create_response.status_code == 201
    order_id = create_response.json()["id"]

    # Mettre à jour la commande
    update_response = await client.put(f"/orders/{order_id}", json={
        "status": "completed"
    })
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["status"] == "completed"

@pytest.mark.asyncio
async def test_delete_order(client):
    # Créer une commande pour le test
    create_response = await client.post("/orders/", json={
        "customer_id": 1,
        "total_amount": 99.99,
        "status": "pending"
    })
    assert create_response.status_code == 201
    order_id = create_response.json()["id"]

    # Supprimer la commande
    delete_response = await client.delete(f"/orders/{order_id}")
    assert delete_response.status_code == 204

    # Vérifier que la commande n'existe plus
    fetch_response = await client.get(f"/orders/{order_id}")
    assert fetch_response.status_code == 404

@pytest.mark.asyncio
async def test_create_order_with_invalid_data(client):
    response = await client.post("/orders/", json={
        "customer_id": "invalid_id",  # ID invalide
        "total_amount": "invalid_amount",  # Montant invalide
        "status": "pending"
    })
    assert response.status_code == 422  # Erreur de validation

@pytest.mark.asyncio
async def test_get_nonexistent_order(client):
    # Tenter de récupérer une commande qui n'existe pas
    response = await client.get("/orders/9999")  # Supposant que l'ID 9999 n'existe pas
    assert response.status_code == 404
