from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict


class TrafficValidator:
    MODERATE_THRESHOLD = 500.0
    CRITICAL_THRESHOLD = 1000.0

    @staticmethod
    def _timestamp() -> str:
        utc_now = datetime.now(timezone.utc).replace(microsecond=0)
        return utc_now.isoformat().replace("+00:00", "Z")

    @classmethod
    def validate_window(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        window_id = str(payload.get("window_id", "")).strip()
        vehicle_count = payload.get("vehicle_count")
        timestamp = payload.get("timestamp")
        location = payload.get("location")

        result = {
            "window_id": window_id,
            "vehicle_count": vehicle_count,
            "timestamp": timestamp,
            "location": location,
            "validated_timestamp": cls._timestamp(),
        }

        try:
            numeric_count = float(vehicle_count)
        except (TypeError, ValueError):
            result.update({"validated": False, "traffic_level": "unknow"})
            return result

        if numeric_count >= cls.CRITICAL_THRESHOLD:
            result.update({"validated": False, "traffic_level": "critical"})
        elif numeric_count >= cls.MODERATE_THRESHOLD:
            result.update({"validated": True, "traffic_level": "moderate"})
        else:
            result.update({"validated": True, "traffic_level": "normal"})

        return result
