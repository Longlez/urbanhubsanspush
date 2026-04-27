from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict


class SensorValidator:
    THRESHOLDS: Dict[str, Dict[str, float]] = {
        "co2": {"moderate": 800.0, "critical": 1000.0},
        "temperature": {"moderate": 35.0, "critical": 40.0},
        "noise": {"moderate": 70.0, "critical": 85.0},
        "pm25": {"moderate": 25.0, "critical": 50.0},
    }

    @classmethod
    def _timestamp(cls) -> str:
        dt = datetime.now(timezone.utc).replace(microsecond=0)
        return dt.isoformat().replace("+00:00", "Z")

    @classmethod
    def classify(cls, sensor: str, value: float) -> Dict[str, Any]:
        normalized_sensor = sensor.strip().lower()
        if normalized_sensor not in cls.THRESHOLDS:
            return {
                "sensor": normalized_sensor,
                "value": value,
                "valid": False,
                "level": "unknown",
                "threshold": None,
                "message": "Capteur inconnu ou non pris en charge.",
                "timestamp": cls._timestamp(),
            }

        thresholds = cls.THRESHOLDS[normalized_sensor]
        if value >= thresholds["critical"]:
            level = "critical"
            valid = False
            message = "Valeur critique détectée. Action immédiate requise."
            threshold = thresholds["critical"]
        elif value >= thresholds["moderate"]:
            level = "moderate"
            valid = True
            message = "Valeur modérée détectée. Surveiller le capteur."
            threshold = thresholds["moderate"]
        else:
            level = "normal"
            valid = True
            message = "Valeur normale."
            threshold = thresholds["moderate"]

        return {
            "sensor": normalized_sensor,
            "value": value,
            "valid": valid,
            "level": level,
            "threshold": threshold,
            "message": message,
            "timestamp": cls._timestamp(),
        }

    @classmethod
    def validate_payload(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        sensor = payload.get("sensor")
        value = payload.get("value")

        if not isinstance(sensor, str) or not sensor.strip():
            return {
                "sensor": sensor,
                "value": value,
                "valid": False,
                "level": "unknown",
                "threshold": None,
                "message": "Le champ 'sensor' doit être une chaîne non vide.",
                "timestamp": cls._timestamp(),
            }

        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            return {
                "sensor": sensor,
                "value": value,
                "valid": False,
                "level": "unknown",
                "threshold": None,
                "message": "Le champ 'value' doit être un nombre valide.",
                "timestamp": cls._timestamp(),
            }

        return cls.classify(sensor, numeric_value)
