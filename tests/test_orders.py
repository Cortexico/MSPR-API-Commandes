from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_order():
    response = client.post("/orders/", json={
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

def test_get_order():
    response = client.post("/orders/", json={
        "customer_id": 1,
        "total_amount": 99.99,
        "status": "pending"
    })
    order_id = response.json()["id"]
    
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["status"] == "pending"
    
def test_update_order():
    response = client.post("/orders/", json={"customer_id": 1, "total_amount": 99.99, "status": "pending"})
    order_id = response.json()["id"]

    update_response = client.put(f"/orders/{order_id}", json={"status": "completed"})
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["status"] == "completed"

def test_delete_order():
    response = client.post("/orders/", json={"customer_id": 1, "total_amount": 99.99, "status": "pending"})
    order_id = response.json()["id"]

    delete_response = client.delete(f"/orders/{order_id}")
    assert delete_response.status_code == 204

    fetch_response = client.get(f"/orders/{order_id}")
    assert fetch_response.status_code == 404

def test_create_order_with_invalid_data():
    response = client.post("/orders/", json={"customer_id": "invalid_id", "total_amount": "99.99", "status": "pending"})
    assert response.status_code == 422  # Assuming 422 for validation errors

def test_get_nonexistent_order():
    response = client.get("/orders/9999")  # Assuming 9999 is an ID that would not exist
    assert response.status_code == 404

