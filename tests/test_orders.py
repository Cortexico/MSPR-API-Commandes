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
