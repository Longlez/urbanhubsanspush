from __future__ import annotations

import json
import os
from typing import Any, Dict

import pika


class RabbitMQClient:
    def __init__(self, host: str | None = None, port: int | None = None) -> None:
        self.host = host or os.getenv("RABBITMQ_HOST", "localhost")
        self.port = port or int(os.getenv("RABBITMQ_PORT", 5672))
        self.connection: pika.BlockingConnection | None = None
        self.channel: pika.adapters.blocking_connection.BlockingChannel | None = None

    def connect(self) -> None:
        if self.connection and self.connection.is_open:
            return

        parameters = pika.ConnectionParameters(host=self.host, port=self.port)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def close(self) -> None:
        if self.connection and self.connection.is_open:
            self.connection.close()
            self.connection = None
            self.channel = None

    def declare_queue(self, queue: str) -> None:
        if self.channel is None:
            self.connect()

        assert self.channel is not None
        self.channel.queue_declare(queue=queue, durable=True)

    def publish(self, payload: Dict[str, Any], queue: str = "validated_queue") -> None:
        if self.channel is None:
            self.connect()

        assert self.channel is not None
        self.declare_queue(queue)
        message = json.dumps(payload)
        self.channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=message.encode("utf-8"),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        self.close()
