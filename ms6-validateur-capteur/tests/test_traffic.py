import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_thresholds_loaded_from_config():
    from src.config.sensor_thresholds import THRESHOLDS

    assert THRESHOLDS["co2"]["moderate"] == 800.0
    assert THRESHOLDS["humidity"]["critical"] == 75.0
    assert THRESHOLDS["pressure"]["moderate"] == 1000.0


def test_traffic_validation_result():
    from src.domain.services import TrafficValidator

    payload = {
        "window_id": "window-123",
        "vehicle_count": 1150,
        "timestamp": "2026-04-27T09:00Z",
        "location": "zone-1",
    }
    validated = TrafficValidator.validate_window(payload)

    assert validated["window_id"] == "window-123"
    assert validated["validated"] is False
    assert validated["traffic_level"] == "critical"
    assert validated["validated_timestamp"].endswith("Z")


def test_traffic_endpoint_publishes_to_validated_queue():
    payload = {
        "window_id": "window-456",
        "vehicle_count": 620,
        "timestamp": "2026-04-27T09:00Z",
        "location": "zone-2",
    }

    with patch("src.adapters.api.routes.RabbitMQClient.publish") as publish_mock:
        response = client.post("/traffic/validate", json=payload)

    assert response.status_code == 200
    publish_mock.assert_called_once()
    data = response.json()
    assert data["traffic_level"] == "moderate"
    assert data["validated"] is True
