import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from src.validator import SensorValidator


def test_validate_normal_co2():
    result = SensorValidator.validate_payload({"sensor": "co2", "value": 500})

    assert result["sensor"] == "co2"
    assert result["value"] == 500.0
    assert result["valid"] is True
    assert result["level"] == "normal"
    assert result["threshold"] == 800.0
    assert result["message"] == "Valeur normale."
    assert result["timestamp"].endswith("Z")


def test_validate_moderate_temperature():
    result = SensorValidator.validate_payload({"sensor": "temperature", "value": 36.5})

    assert result["sensor"] == "temperature"
    assert result["valid"] is True
    assert result["level"] == "moderate"
    assert result["threshold"] == 35.0
    assert "modérée" in result["message"]


def test_validate_critical_noise():
    result = SensorValidator.validate_payload({"sensor": "noise", "value": 90})

    assert result["sensor"] == "noise"
    assert result["valid"] is False
    assert result["level"] == "critical"
    assert result["threshold"] == 85.0
    assert "critique" in result["message"]


def test_validate_unknown_sensor():
    result = SensorValidator.validate_payload(
        {"sensor": "unknown_sensor", "value": 100}
    )

    assert result["sensor"] == "unknown_sensor"
    assert result["valid"] is False
    assert result["level"] == "unknown"
    assert result["threshold"] is None
    assert "inconnu" in result["message"]
