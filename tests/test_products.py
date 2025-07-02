from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
auth = ("admin", "admin123")  # from .env

def test_create_product():
    response = client.post("/api/v1/products/", json={
        "name": "Test Product",
        "description": "FastAPI test",
        "price": 10.5,
        "in_stock": True
    }, auth=auth)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert "id" in data

    # Save ID for later tests
    global created_product_id
    created_product_id = data["id"]

def test_get_all_products():
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product_by_id():
    global created_product_id
    response = client.get(f"/api/v1/products/{created_product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == created_product_id

def test_update_product():
    global created_product_id
    response = client.put(f"/api/v1/products/{created_product_id}", json={
        "name": "Updated Product",
        "description": "Updated desc",
        "price": 20.0,
        "in_stock": False
    }, auth=auth)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"

def test_delete_product():
    global created_product_id
    response = client.delete(f"/api/v1/products/{created_product_id}", auth=auth)
    assert response.status_code == 204

    # Confirm deletion
    response = client.get(f"/api/v1/products/{created_product_id}")
    assert response.status_code == 404
