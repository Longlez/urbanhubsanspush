# Premier lancement

Ce tutoriel montre comment lancer le microservice `ms6-validateur-capteur` en local.

## Prérequis

- Python 3.11
- Docker (pour l'exécution en conteneur)
- RabbitMQ si vous souhaitez tester l'endpoint de publication

## Installation

```bash
cd ms6-validateur-capteur
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Exécution en mode API

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Tester l'API

```bash
curl -X POST http://localhost:8000/validate \
  -H 'Content-Type: application/json' \
  -d '{"sensor": "co2", "value": 500}'
```
