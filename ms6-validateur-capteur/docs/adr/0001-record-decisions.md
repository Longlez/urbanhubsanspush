# ADR 0001: Architecture du microservice ms6-validateur-capteur

## Contexte

Le microservice doit valider les données de capteurs et les fenêtres de trafic avant publication vers RabbitMQ.

## Décision

- Utiliser FastAPI pour exposer les endpoints HTTP.
- Séparer les seuils de capteurs dans `src/config/sensor_thresholds.py`.
- Isoler la logique métier dans `src/domain/`.
- Isoler les adaptateurs API et RabbitMQ dans `src/adapters/`.
- Exposer un endpoint `POST /validate` et un endpoint `POST /traffic/validate`.
