"""
Point d'entrée du microservice Journalisation
"""
import json
import os
from typing import Callable
from src.application.process_log_use_case import ProcessLogUseCase
from src.adapters.api.log_api_adapter import LogApiAdapter
from src.adapters.database.log_repository_adapter import InMemoryLogRepository
from src.adapters.database.log_validator_adapter import LogValidator
from src.adapters.rabbitmq.log_consumer_adapter import MockLogConsumer, RabbitMQLogConsumer


def main():
    """Point d'entrée principal du microservice"""

    # Initialisation des adapters
    log_repository = InMemoryLogRepository()
    log_validator = LogValidator()

    # Initialisation du use case
    process_log_use_case = ProcessLogUseCase(log_repository, log_validator)

    # Initialisation de l'API de consultation
    log_api_adapter = LogApiAdapter(process_log_use_case)

    # Choix du consumer : mock en local/test ou RabbitMQ en production
    use_mock = os.environ.get("USE_MOCK_CONSUMER", "true").lower() == "true"
    rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")

    log_consumer = MockLogConsumer() if use_mock else RabbitMQLogConsumer(host=rabbitmq_host)

    def handle_message(message: str) -> None:
        """Traite un message reçu de RabbitMQ ou via le mock consumer"""
        try:
            log_data = json.loads(message)
            success, msg, log_id = process_log_use_case.execute(log_data)
            if success:
                print(f"✓ Log processed: {log_id}")
            else:
                print(f"✗ Error: {msg}")
        except json.JSONDecodeError as e:
            print(f"✗ Invalid JSON: {e}")
        except Exception as e:
            print(f"✗ Error processing message: {e}")

    # Exemple de logs à publier
    sample_logs = [
        {"service": "MS Journalisation", "event_type": "startup", "message": "Service started", "level": "INFO"},
        {"service": "MS Journalisation", "event_type": "health_check", "message": "Health check OK", "level": "INFO"},
        {"service": "MS Journalisation", "event_type": "error_event", "message": "Example error", "level": "ERROR"},
    ]

    print("Starting Log Microservice...")
    log_consumer.start(handle_message)

    for log_data in sample_logs:
        log_consumer.publish_message(json.dumps(log_data))

    # Consulter les logs via l'API adapter
    log_api_adapter.get_all_logs()
    log_api_adapter.get_logs_by_level("ERROR")

    log_consumer.stop()


if __name__ == "__main__":
    main()
