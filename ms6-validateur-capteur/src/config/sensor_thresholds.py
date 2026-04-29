from __future__ import annotations

from typing import Dict

THRESHOLDS: Dict[str, Dict[str, float]] = {
    "co2": {"moderate": 800.0, "critical": 1000.0},
    "temperature": {"moderate": 35.0, "critical": 40.0},
    "noise": {"moderate": 70.0, "critical": 85.0},
    "humidity": {"moderate": 60.0, "critical": 75.0},
    "pressure": {"moderate": 1000.0, "critical": 1200.0},
}
