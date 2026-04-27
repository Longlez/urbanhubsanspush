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


def test_capteur_ajouté():
    # Test ajout d'un nouveau capteur
    success = SensorValidator.add_sensor("humidity", 60.0, 80.0)
    assert success is True

    # Test que le capteur ajouté fonctionne
    result = SensorValidator.validate_payload({"sensor": "humidity", "value": 50})
    assert result["sensor"] == "humidity"
    assert result["valid"] is True
    assert result["level"] == "normal"

    # Test seuil modéré
    result = SensorValidator.validate_payload({"sensor": "humidity", "value": 65})
    assert result["level"] == "moderate"

    # Test seuil critique
    result = SensorValidator.validate_payload({"sensor": "humidity", "value": 85})
    assert result["level"] == "critical"
    assert result["valid"] is False


def test_validate_payload_sensor_invalid():
    # Test sensor vide
    result = SensorValidator.validate_payload({"sensor": "", "value": 100})
    assert result["valid"] is False
    assert result["level"] == "unknown"
    assert "non vide" in result["message"]

    # Test sensor non string
    result = SensorValidator.validate_payload({"sensor": 123, "value": 100})
    assert result["valid"] is False
    assert result["level"] == "unknown"
    assert "chaîne non vide" in result["message"]


def test_validate_payload_value_invalid():
    # Test value non numérique
    result = SensorValidator.validate_payload({"sensor": "co2", "value": "invalid"})
    assert result["valid"] is False
    assert result["level"] == "unknown"
    assert "nombre valide" in result["message"]

    # Test value None
    result = SensorValidator.validate_payload({"sensor": "co2", "value": None})
    assert result["valid"] is False
    assert result["level"] == "unknown"
    assert "nombre valide" in result["message"]


def test_add_sensor_invalid_thresholds():
    # Test seuils invalides (moderate >= critical)
    success = SensorValidator.add_sensor("test_sensor", 80.0, 70.0)
    assert success is False

    # Test seuils égaux
    success = SensorValidator.add_sensor("test_sensor2", 80.0, 80.0)
    assert success is False


def test_add_sensor_already_exists():
    # Test ajout d'un capteur qui existe déjà
    success = SensorValidator.add_sensor("co2", 100.0, 200.0)
    assert success is False
