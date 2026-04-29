# Architecture

`ms6-validateur-capteur` est un microservice FastAPI dédié à la validation des données de capteurs et des fenêtres de trafic.

- `src/adapters/api/routes.py` expose les endpoints HTTP.
- `src/domain/sensor_validation.py` contient la logique métier de classification des capteurs.
- `src/domain/services.py` contient la logique de validation et enrichissement des fenêtres de trafic.
- `src/adapters/rabbitmq/client.py` publie les messages validés vers RabbitMQ.
