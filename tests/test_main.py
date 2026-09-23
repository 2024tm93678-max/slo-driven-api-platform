import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
    
    
def test_get_products():
    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 3
    
    
def test_create_product():
    response = client.post(
        "/products",
        json={
            "name": "Monitor",
            "price": 15000
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Monitor"
    assert data["price"] == 15000
    
def test_rejects_empty_product_name():
    response = client.post(
        "/products",
        json={
            "name": "",
            "price": 15000
        }
    )

    assert response.status_code == 422
    
def test_rejects_negative_product_price():
    response = client.post(
        "/products",
        json={
            "name": "Invalid Product",
            "price": -100
        }
    )

    assert response.status_code == 422
    
def test_create_order():
    response = client.post(
        "/orders",
        json={
            "product_id": 1,
            "quantity": 2
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 1
    assert data["quantity"] == 2
    assert data["status"] == "created"


def test_get_orders():
    response = client.get("/orders")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    
def test_process_order():
    response = client.post(
        "/worker",
        json={
            "order_id": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["order_id"] == 1
    assert data["status"] == "processed"


def test_get_jobs():
    response = client.get("/worker")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)