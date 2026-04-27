from fastapi import FastAPI
from pydantic import BaseModel, Field

from .validator import SensorValidator

app = FastAPI(title="MS6 Validateur Capteur", version="1.0.0")


class SensorPayload(BaseModel):
    sensor: str = Field(..., example="co2")
    value: float = Field(..., example=650.0)


@app.post("/validate")
def validate_sensor(payload: SensorPayload) -> dict:
    return SensorValidator.validate_payload(payload.dict())


@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "service": "ms6-validateur-capteur"}
