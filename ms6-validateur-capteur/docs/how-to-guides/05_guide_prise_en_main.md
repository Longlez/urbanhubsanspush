# Guide de prise en main pour nouveaux développeurs

Bienvenue dans l'équipe UrbanHub ! Ce guide vous accompagnera pour prendre en main le microservice `ms6-validateur-capteur` et contribuer efficacement au projet.

## Prérequis système

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.12** (version exacte utilisée en production)
- **Docker** et **Docker Compose** pour l'environnement local
- **Git** pour le versioning
- **Un éditeur** comme VS Code avec extensions Python

## Clonage et configuration initiale

1. **Clonez le repository** :
   ```bash
   git clone https://github.com/votre-org/UrbanHub.git
   cd UrbanHub
   ```

2. **Créez un environnement virtuel** :
   ```bash
   python -m venv .venv
   # Sur Windows
   .venv\Scripts\activate
   # Sur Linux/Mac
   source .venv/bin/activate
   ```

3. **Installez les dépendances** :
   ```bash
   cd ms6-validateur-capteur
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## Structure du projet

Comprenez l'organisation des fichiers :

```
ms6-validateur-capteur/
├── src/                    # Code source
│   ├── adapters/          # Couche d'adaptation (API, RabbitMQ)
│   ├── domain/            # Logique métier
│   └── config/            # Configuration
├── tests/                 # Tests unitaires
├── docs/                  # Documentation Diátaxis
├── requirements.txt       # Dépendances production
└── requirements-dev.txt   # Dépendances développement
```

## Premier lancement

1. **Démarrez les services avec Docker Compose** :
   ```bash
   docker compose up -d rabbitmq
   ```

2. **Lancez le microservice** :
   ```bash
   python -m src.main
   ```

3. **Vérifiez que ça fonctionne** :
   ```bash
   curl http://localhost:8000/health
   ```

## Développement quotidien

### Tests

- **Lancez tous les tests** : `pytest`
- **Avec couverture** : `pytest --cov=src`
- **Tests spécifiques** : `pytest tests/test_validator.py`

### Qualité du code

- **Linting** : `flake8 src tests`
- **Formatage** : `black src tests`

### Débogage

- Utilisez les endpoints de test :
  ```bash
  # Test validation capteur
  curl -X POST http://localhost:8000/validate \
    -H "Content-Type: application/json" \
    -d '{"sensor_id": "test", "co2": 400, "temperature": 20}'
  ```

## Contribution au code

1. **Créez une branche** :
   ```bash
   git checkout -b feature/ma-nouvelle-fonction
   ```

2. **Écrivez des tests** avant le code (TDD)

3. **Implémentez la fonctionnalité**

4. **Vérifiez la qualité** :
   - Tests passent : `pytest`
   - Code propre : `flake8`
   - Couverture > 80%

5. **Commitez avec des messages clairs** :
   ```bash
   git commit -m "feat: ajouter validation température critique"
   ```

## Déploiement local

Pour tester le déploiement complet :

```bash
# Construire l'image
docker build -t ms6-validateur-capteur .

# Lancer avec compose
docker compose up ms6-validateur-capteur
```

## Ressources utiles

- **Documentation API** : `http://localhost:8000/docs` (Swagger UI)
- **Logs** : Consultez les logs Docker pour le debugging
- **Tests** : Les rapports se trouvent dans `03_rapport_tests/`
- **Équipe** : Posez vos questions sur Slack #dev-urbanhub

## Dépannage courant

- **Erreur de dépendances** : `pip install --upgrade pip` puis réinstaller
- **Port occupé** : Vérifiez que rien n'écoute sur 8000
- **Tests qui échouent** : Lancez `pytest -v` pour détails
- **RabbitMQ inaccessible** : `docker compose logs rabbitmq`

N'hésitez pas à demander de l'aide à l'équipe si vous êtes bloqué. Bonne intégration !