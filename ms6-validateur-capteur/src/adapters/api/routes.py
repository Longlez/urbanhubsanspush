from __future__ import annotations

import os
from fastapi import APIRouter, BackgroundTasks

from ..rabbitmq.client import RabbitMQClient
from ...domain.sensor_validation import SensorValidator
from ...domain.services import TrafficValidator
from .schemas import SensorPayload, TrafficPayload


router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "service": "ms6-validateur-capteur"}


@router.post("/validate")
def validate_sensor(payload: SensorPayload) -> dict:
    return SensorValidator.validate_payload(payload.model_dump())


@router.post("/traffic/validate")
def validate_traffic(payload: TrafficPayload, background_tasks: BackgroundTasks) -> dict:
    validated_payload = TrafficValidator.validate_window(payload.model_dump())
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
    output_queue = os.getenv("RABBITMQ_OUTPUT_QUEUE", "validated_queue")
    background_tasks.add_task(
        RabbitMQClient(host=rabbitmq_host).publish,
        validated_payload,
        output_queue,
    )
    return validated_payload
