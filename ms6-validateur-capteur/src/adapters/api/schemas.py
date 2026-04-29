from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class SensorPayload(BaseModel):
    sensor: str = Field(..., json_schema_extra={"example": "co2"})
    value: float = Field(..., json_schema_extra={"example": 500.0})


class TrafficPayload(BaseModel):
    window_id: str = Field(..., json_schema_extra={"example": "window-123"})
    vehicle_count: float = Field(..., json_schema_extra={"example": 720.0})
    timestamp: str = Field(..., json_schema_extra={"example": "2026-04-27T09:00Z"})
    location: Optional[str] = Field(None, json_schema_extra={"example": "zone-1"})
