import os
import sys
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from src.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "ms6-validateur-capteur"


def test_validate_endpoint_normal():
    payload = {"sensor": "co2", "value": 500.0}
    response = client.post("/validate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["sensor"] == "co2"
    assert data["value"] == 500.0
    assert data["valid"] is True
    assert data["level"] == "normal"


def test_validate_endpoint_moderate():
    payload = {"sensor": "temperature", "value": 36.5}
    response = client.post("/validate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["sensor"] == "temperature"
    assert data["valid"] is True
    assert data["level"] == "moderate"


def test_validate_endpoint_critical():
    payload = {"sensor": "noise", "value": 90.0}
    response = client.post("/validate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["sensor"] == "noise"
    assert data["valid"] is False
    assert data["level"] == "critical"


def test_validate_endpoint_unknown_sensor():
    payload = {"sensor": "unknown", "value": 100.0}
    response = client.post("/validate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["sensor"] == "unknown"
    assert data["valid"] is False
    assert data["level"] == "unknow"


def test_validate_endpoint_invalid_sensor():
    payload = {"sensor": "", "value": 100.0}
    response = client.post("/validate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert data["level"] == "unknow"
    assert "non vide" in data["message"]


def test_validate_endpoint_invalid_value():
    payload = {"sensor": "co2", "value": "invalid"}
    response = client.post("/validate", json=payload)
    # Pydantic retourne 422 pour les données invalides avant notre logique de validation
    assert response.status_code == 422