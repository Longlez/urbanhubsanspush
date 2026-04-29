from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from ..config.sensor_thresholds import THRESHOLDS


class SensorValidator:
    THRESHOLDS = THRESHOLDS

    @staticmethod
    def _timestamp() -> str:
        utc_now = datetime.now(timezone.utc).replace(microsecond=0)
        return utc_now.isoformat().replace("+00:00", "Z")

    @classmethod
    def classify(cls, sensor: str, value: float) -> Dict[str, Any]:
        normalized_sensor = sensor.strip().lower()
        thresholds = cls.THRESHOLDS.get(normalized_sensor)

        if thresholds is None:
            return {
                "sensor": normalized_sensor,
                "value": value,
                "valid": False,
                "level": "unknow",
                "threshold": None,
                "message": "Capteur inconnu ou non pris en charge.",
                "timestamp": cls._timestamp(),
            }

        if value >= thresholds["critical"]:
            return {
                "sensor": normalized_sensor,
                "value": value,
                "valid": False,
                "level": "critical",
                "threshold": thresholds["critical"],
                "message": "Valeur critique détectée. Action immédiate requise.",
                "timestamp": cls._timestamp(),
            }

        if value >= thresholds["moderate"]:
            return {
                "sensor": normalized_sensor,
                "value": value,
                "valid": True,
                "level": "moderate",
                "threshold": thresholds["moderate"],
                "message": "Valeur modérée détectée. Surveiller le capteur.",
                "timestamp": cls._timestamp(),
            }

        return {
            "sensor": normalized_sensor,
            "value": value,
            "valid": True,
            "level": "normal",
            "threshold": thresholds["moderate"],
            "message": "Valeur normale.",
            "timestamp": cls._timestamp(),
        }

    @classmethod
    def add_sensor(cls, sensor_name: str, moderate_threshold: float, critical_threshold: float) -> bool:
        normalized_sensor = sensor_name.strip().lower()
        if normalized_sensor in cls.THRESHOLDS:
            return False

        if moderate_threshold >= critical_threshold:
            return False

        cls.THRESHOLDS[normalized_sensor] = {
            "moderate": moderate_threshold,
            "critical": critical_threshold,
        }
        return True

    @classmethod
    def validate_payload(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        sensor = payload.get("sensor")
        value = payload.get("value")

        if not isinstance(sensor, str) or not sensor.strip():
            return {
                "sensor": sensor,
                "value": value,
                "valid": False,
                "level": "unknow",
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
                "level": "unknow",
                "threshold": None,
                "message": "Le champ 'value' doit être un nombre valide.",
                "timestamp": cls._timestamp(),
            }

        return cls.classify(sensor, numeric_value)
