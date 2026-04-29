# Dockeriser le service

Ce guide décrit comment construire et exécuter l'image Docker du service.

## Construction

```bash
docker build -t ms6-validateur-capteur:local .
```

## Exécution

```bash
docker run --rm -p 8000:8000 ms6-validateur-capteur:local
```

## Vérification

```bash
curl http://localhost:8000/health
```
