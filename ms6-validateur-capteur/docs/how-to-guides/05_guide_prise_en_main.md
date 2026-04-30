# Guide de prise en main pour les nouveaux développeurs

Bienvenue dans l'équipe UrbanHub ! Ce guide vous accompagnera pour prendre en main le microservice `ms6-validateur-capteur` et contribuer efficacement au projet.

## Prérequis système

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.12** (version exacte utilisée en production)
- **Docker** et **Docker Compose** pour l'environnement local
- **Git** pour le versioning
- **Un éditeur** comme VS Code avec extensions Python

## 1. Clonage du dépôt et positionnement sur la branche

1. **Clonez le repository** :
   ```bash
   git clone https://github.com/votre-org/UrbanHub.git
   cd UrbanHub
   ```

2. **Positionnez-vous sur la branche appropriée** :
   ```bash
   # Pour développement
   git checkout develop

   # Pour production (avec prudence)
   git checkout main
   ```

3. **Créez votre branche de travail** :
   ```bash
   git checkout -b feature/votre-nom-fonctionnalite
   ```

## 2. Installation des dépendances

Après avoir cloné et activé votre environnement virtuel :

```bash
cd ms6-validateur-capteur

# Commande exacte pour installer les dépendances
pip install -r requirements.txt -r requirements-dev.txt
```

Cette commande installe :
- Les dépendances de production (`requirements.txt`)
- Les outils de développement (`requirements-dev.txt` : pytest, flake8, etc.)

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

3. **Vérifiez que ça fonctionne** (healthcheck) :
   ```bash
   curl http://localhost:8006/health
   ```
   **Résultat attendu** : `{"status": "healthy"}`

## 3. Lancement des tests en local

### Commande exacte pour lancer tous les tests :
```bash
pytest
```

### Résultat attendu :
- **Nombre de tests** : 19 tests passent
- **Couverture** : Au moins 80%
- **Rapports générés** :
  - `03_rapport_tests/rapport_tests.xml`
  - `03_rapport_tests/coverage.xml`

### Tests avec couverture détaillée :
```bash
pytest --cov=src --cov-report=html
```

### Tests spécifiques :
```bash
# Tests de validation
pytest tests/test_validator.py

# Tests de trafic
pytest tests/test_traffic.py

# Tests d'API
pytest tests/test_main.py
```

## Développement quotidien

### Qualité du code

- **Linting** : `flake8 src tests`
- **Formatage** : `black src tests`

### Débogage

- Utilisez les endpoints de test :
  ```bash
  # Test validation capteur
  curl -X POST http://localhost:8006/validate \
    -H "Content-Type: application/json" \
    -d '{"sensor_id": "test", "co2": 400, "temperature": 20}'
  ```

## 4. GitHub Secrets requis

Pour contribuer au projet, vous devez configurer les secrets suivants dans les paramètres GitHub du repository (Settings > Secrets and variables > Actions) :

| Secret | Rôle |
|--------|------|
| `SNYK_TOKEN` | Authentification pour les scans de sécurité Snyk (analyse des vulnérabilités dans les dépendances) |
| `GHCR_TOKEN` | Authentification pour pousser les images Docker vers GitHub Container Registry |

**Note** : Ces secrets sont configurés au niveau repository et utilisés par le pipeline CI/CD. Vous n'avez pas besoin de connaître leurs valeurs, seulement de savoir qu'ils existent pour que le pipeline fonctionne.

## 5. Procédure pour ajouter un nouveau capteur dans Thresholds

Pour ajouter un nouveau type de capteur avec ses seuils de validation :

1. **Ouvrez le fichier de configuration** :
   ```bash
   # Éditez le fichier des seuils
   nano src/config/sensor_thresholds.py
   ```

2. **Ajoutez le nouveau capteur** :
   ```python
   THRESHOLDS = {
       # Capteurs existants...
       "co2": {"min": 300, "max": 2000},
       "temperature": {"min": 10, "max": 35},
       "noise": {"min": 30, "max": 100},
       "humidity": {"min": 20, "max": 80},
       "pressure": {"min": 950, "max": 1050},

       # Nouveau capteur - exemple pour particules fines
       "pm25": {"min": 0, "max": 50}
   }
   ```

3. **Mettez à jour la logique de validation** :
   - Éditez `src/domain/sensor_validation.py`
   - Ajoutez la logique spécifique dans `validate_sensor()` ou créez une méthode dédiée

4. **Ajoutez des tests** :
   ```bash
   # Dans tests/test_validator.py
   def test_pm25_validation():
       # Test pour le nouveau capteur PM2.5
   ```

5. **Testez localement** :
   ```bash
   pytest tests/test_validator.py
   ```

6. **Commitez vos changements** :
   ```bash
   git add .
   git commit -m "feat: ajouter support capteur PM2.5 avec seuils"
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

**Note** : Le service sera accessible sur le port 8006 avec healthcheck `/health`.

## Ressources utiles

- **Documentation API** : `http://localhost:8006/docs` (Swagger UI)
- **Logs** : Consultez les logs Docker pour le debugging
- **Tests** : Les rapports se trouvent dans `03_rapport_tests/`
- **Équipe** : Posez vos questions sur Slack #dev-urbanhub

## Dépannage courant

- **Erreur de dépendances** : `pip install --upgrade pip` puis réinstaller
- **Port occupé** : Vérifiez que rien n'écoute sur 8006
- **Tests qui échouent** : Lancez `pytest -v` pour détails
- **RabbitMQ inaccessible** : `docker compose logs rabbitmq`

N'hésitez pas à demander de l'aide à l'équipe si vous êtes bloqué.