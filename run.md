# Guide d'exécution - UrbanHub

Ce fichier rassemble toutes les commandes pour exécuter les microservices, lancer les tests et générer les rapports de couverture.

## 1. Préparation de l'environnement

### Créer un environnement Python
```bash
cd c:\Users\raval\Documents\UrbanHubFork
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Installer les dépendances globales
```bash
pip install -r ms-analyse/requirements.txt
pip install -r ms-analyse/requirements-dev.txt
pip install -r ms-collecte-iot/requirements.txt
pip install -r ms-journalisation/requirements.txt
pip install -r ms-alerte-usager/requirements.txt
```

> Si `requirements-dev.txt` n'existe pas pour un microservice, installez seulement `requirements.txt`.

## 2. Commandes d'exécution par microservice

### 2.1 ms-analyse

Ce service expose une API FastAPI.

```bash
cd c:\Users\raval\Documents\UrbanHubFork\ms-analyse
uvicorn src.main:app --reload --host 0.0.0.0 --port 8001
```

#### Variables d'environnement utiles
```powershell
$env:DATABASE_URL="sqlite:///./ms_analyse.db"
$env:ENABLE_RABBITMQ_CONSUMER="true"
```

### 2.2 ms-collecte-iot

Ce service démarre un consommateur RabbitMQ et normalise les données.

```bash
cd c:\Users\raval\Documents\UrbanHubFork\ms-collecte-iot
python src/main.py
```

#### Variables d'environnement utiles
```powershell
$env:MONGODB_URI="mongodb://localhost:27017"
$env:MONGODB_DATABASE="urbanhub"
$env:MONGODB_COLLECTION="iot_collecte"
```

### 2.3 ms-journalisation

Service de traitement des logs via RabbitMQ.

```bash
cd c:\Users\raval\Documents\UrbanHubFork\ms-journalisation
python src/main.py
```

#### Variables d'environnement utiles
```powershell
$env:RABBITMQ_HOST="localhost"
```

### 2.4 ms-alerte-usager

Service d'alerte utilisateur avec consommation RabbitMQ.

```bash
cd c:\Users\raval\Documents\UrbanHubFork\ms-alerte-usager
python src/main.py
```

#### Variables d'environnement utiles
```powershell
$env:DATABASE_URL="postgresql://user:password@localhost:5432/alerts"
```

## 3. Commandes de test

### 3.1 ms-analyse

```bash
cd c:\Users\raval\Documents\UrbanHubFork\ms-analyse
pytest tests/ --junitxml=..\rapport_tests\ms-analyse_tests.xml --cov=src --cov-report=xml:..\rapport_tests\ms-analyse_coverage.xml
```

### 3.2 ms-collecte-iot

```bash
cd c:\Users\raval\Documents\UrbanHubFork\ms-collecte-iot
pytest test/unit --junitxml=..\rapport_tests\ms-collecte-iot_tests.xml --cov=src --cov-report=xml:..\rapport_tests\ms-collecte-iot_coverage.xml
```

### 3.3 ms-journalisation

```bash
cd c:\Users\raval\Documents\UrbanHubFork\ms-journalisation
pytest tests/ --junitxml=..\rapport_tests\ms-journalisation_tests.xml --cov=src --cov-report=xml:..\rapport_tests\ms-journalisation_coverage.xml
```

### 3.4 ms-alerte-usager

```bash
cd c:\Users\raval\Documents\UrbanHubFork\ms-alerte-usager
pytest test/unit --junitxml=..\rapport_tests\ms-alerte-usager_tests.xml --cov=src --cov-report=xml:..\rapport_tests\ms-alerte-usager_coverage.xml
```

> Si `pytest` échoue à cause de dépendances manquantes, installez les packages requis dans `.venv`.

## 4. Génération de rapports de couverture

### Couverture consolidée par microservice
- `rapport_tests/ms-analyse_coverage.xml`
- `rapport_tests/ms-collecte-iot_coverage.xml`
- `rapport_tests/ms-journalisation_coverage.xml`
- `rapport_tests/ms-alerte-usager_coverage.xml`

### Rapport de tests JUnit
- `rapport_tests/ms-analyse_tests.xml`
- `rapport_tests/ms-collecte-iot_tests.xml`
- `rapport_tests/ms-journalisation_tests.xml`
- `rapport_tests/ms-alerte-usager_tests.xml`

### Générer un rapport texte si besoin
```bash
cd c:\Users\raval\Documents\UrbanHubFork
pytest --junitxml=rapport_tests/combined_tests.xml --cov=./ --cov-report=xml:rapport_tests/combined_coverage.xml
```

## 5. Docker et orchestration

### Construire les images Docker
```bash
cd c:\Users\raval\Documents\UrbanHubFork
docker-compose build
```

### Lancer tous les services
```bash
cd c:\Users\raval\Documents\UrbanHubFork
docker-compose up -d
```

### Arrêter les services
```bash
docker-compose down
```

## 6. Commandes utiles supplémentaires

### Vérifier l'état des containers
```bash
docker-compose ps
```

### Voir les logs d'un service
```bash
docker-compose logs -f <service_name>
```

### Nettoyer l'environnement Docker
```bash
docker-compose down --volumes --remove-orphans
```

---

## Notes
- Exécutez chaque commande depuis la racine du projet ou depuis le dossier du microservice indiqué.
- Les chemins Windows utilisent des backslashes (`\`). Adaptez-les si vous travaillez dans un shell UNIX.
- Vérifiez que RabbitMQ et MongoDB sont démarrés avant de lancer les microservices qui en dépendent.
