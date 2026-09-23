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
    
from app.slo.evaluator import evaluate_slo
from app.slo.gate import should_rollback


def test_slo_passes_when_metrics_are_within_thresholds():
    result = evaluate_slo(
        error_rate=0.005,
        p95_latency_ms=250
    )

    assert result["error_rate_pass"] is True
    assert result["latency_pass"] is True
    assert result["slo_pass"] is True


def test_slo_fails_when_error_rate_exceeds_threshold():
    result = evaluate_slo(
        error_rate=0.02,
        p95_latency_ms=250
    )

    assert result["error_rate_pass"] is False
    assert result["latency_pass"] is True
    assert result["slo_pass"] is False


def test_slo_fails_when_latency_exceeds_threshold():
    result = evaluate_slo(
        error_rate=0.005,
        p95_latency_ms=350
    )

    assert result["error_rate_pass"] is True
    assert result["latency_pass"] is False
    assert result["slo_pass"] is False


def test_rollback_requires_two_consecutive_failures():
    assert should_rollback(1) is False
    assert should_rollback(2) is True
    assert should_rollback(3) is True
    
def test_metrics_endpoint():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "http_requests_total" in response.text
    assert "http_request_latency_seconds" in response.text