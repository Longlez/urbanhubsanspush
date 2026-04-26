# L5 — Documentation GitHub pour MS Journalisation

Cette documentation est destinée à GitHub Wiki/Pages et couvre les aspects clés du microservice Journalisation.

---

## 1. Vue d'ensemble

### Présentation générale

Le **MS Journalisation** est un microservice centralisé du projet UrbanHub, conçu pour collecter, valider et stocker les logs de tous les autres microservices du système. Il suit une **architecture hexagonale (Ports & Adapters)** pour assurer une séparation claire entre la logique métier et les composants techniques.

### Objectif

Fournir un point unique de collecte et de consultation des logs, permettant à tous les microservices de :
- Envoyer leurs logs via **RabbitMQ**
- Accéder aux logs via une **API REST**
- Bénéficier d'une **validation centralisée** et d'un **enrichissement des métadonnées**

### Architecture hexagonale

```
┌─────────────────────────────────────────┐
│         Couche Application              │
│     (ProcessLogUseCase)                 │
└─────────────────────────────────────────┘
         ↓              ↓              ↓
    Repository      Consumer       Validator
    (Port)          (Port)         (Port)
         ↓              ↓              ↓
┌──────────────┬──────────────┬──────────────┐
│     DB       │   RabbitMQ   │  Validation  │
│   (Adapter)  │   (Adapter)  │   (Adapter)  │
└──────────────┴──────────────┴──────────────┘
```

### Flux de données

```
RabbitMQ (LogConsumer)
    ↓
Validation (LogValidator)
    ↓
Transformation → Log (Domain)
    ↓
Use Case (ProcessLogUseCase)
    ↓
Persistance (LogRepository)
    ↓
API REST (LogApiAdapter)
```

---

## 2. Étapes (Pipeline CI/CD)

### Workflow GitHub Actions

Le pipeline `.github/workflows/workflow.yml` comprend 5 étapes clés :

#### Étape 1 : Checkout
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
```

#### Étape 2 : Setup et dépendances
```yaml
- name: Setup Python and install dependencies
  uses: actions/setup-python@v5
  with:
    python-version: 3.12
```

#### Étape 3 : Tests unitaires + Couverture
```yaml
- name: Run unit tests with coverage
  run: |
    pip install -r requirements.txt
    pytest --junitxml=rapport_tests.xml \
      --cov=src \
      --cov-report=xml \
      --cov-report=html:coverage_html
```

#### Étape 4 : Analyse SonarQube
```yaml
- name: Run SonarQube analysis
  uses: SonarSource/sonarqube-scan-action@v6
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
    SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

#### Étape 5 : Scan Snyk
```yaml
- name: Run Snyk security scan
  uses: snyk/actions/python@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
  with:
    args: test --file=requirements.txt --severity-threshold=high
```

### Déclenchement

Le pipeline s'exécute automatiquement sur :
- **Push** sur `main` ou `develop` dans le dossier `ms-journalisation/**`
- **Pull Request** vers `main` ou `develop` dans le dossier `ms-journalisation/**`

### Uploads d'artefacts

À chaque run, les rapports suivants sont uploadés :
- `rapport_tests.txt`
- `rapport_tests.xml`
- `coverage_html/`
- `coverage.xml`

---

## 3. Outils

### Langage et runtime
- **Python 3.12** : langage principal du microservice

### Dépendances de production
- **pika 1.3.1** : client RabbitMQ
- **python-dotenv 1.0.0** : gestion des variables d'environnement

### Dépendances de développement
- **pytest 7.4.0** : framework de test unitaire
- **pytest-cov 4.1.0** : plugin de couverture de code

### Outils de qualité (CI)
- **GitHub Actions** : orchestration des pipelines
- **SonarQube** : analyse statique du code
- **Snyk** : scan de vulnérabilités dans les dépendances
- **Coverage.py** : rapport de couverture du code

### Outils de déploiement
- **Docker** : containerisation
- **Docker Registry** : stockage des images

### Outils de développement
- **Bash/Python** : scripts réutilisables pour build, test, déploiement

---

## 4. Prérequis

### Environnement local

1. **Python 3.12+**
   ```bash
   python --version
   ```

2. **pip** (gestionnaire de paquets Python)
   ```bash
   pip --version
   ```

3. **RabbitMQ** (optionnel, utilise un mock en tests)
   ```bash
   docker run -d --rm -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
   ```

4. **Git**
   ```bash
   git --version
   ```

### Configuration GitHub

Pour que le pipeline fonctionne, ajouter les secrets GitHub sous `Settings → Secrets and variables → Actions` :

- `SONAR_HOST_URL` : URL du serveur SonarQube (ex. `https://sonarcloud.io`)
- `SONAR_TOKEN` : Token d'authentification SonarQube
- `SNYK_TOKEN` : Token d'authentification Snyk

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/your-org/urbanhub.git
cd urbanhub/ms-journalisation

# Installer les dépendances
pip install -r requirements.txt
```

---

## 5. Qualité et dette technique

### Métriques de qualité

Le projet suit les standards suivants :

| Métrique | Seuil | Outil |
|----------|-------|-------|
| Couverture de code | ≥ 80% | pytest-cov |
| Vulnérabilités critiques | 0 | Snyk |
| Bugs/Vulnérabilités critiques | 0 | SonarQube |
| Densité de code smell | Acceptable | SonarQube |

### Tests

- **55 tests unitaires** : 100% de succès
- Couvrage estimé : **80%+** du code source
- Tous les domaines testés :
  - Domain (15 tests)
  - Application (15 tests)
  - Adapters (25+ tests)

### Analyse de la dette technique

#### État actuel : Faible

- **Code** : Aucun défaut critique, architecture propre et bien testée
- **Dépendances** : Pika et python-dotenv stables et maintenues
- **Documentation** : Complète avec README, docstrings et commentaires

#### Actions de maintenance

1. Mettre à jour les dépendances régulièrement
   ```bash
   pip install --upgrade pika python-dotenv
   ```

2. Exécuter les tests avant chaque commit
   ```bash
   pytest
   ```

3. Vérifier la couverture
   ```bash
   pytest --cov=src --cov-report=term-missing
   ```

---

## 6. Intégration UrbanHub

### Architecture globale

MS Journalisation s'intègre dans l'écosystème UrbanHub comme **service centralisé de logging** :

```
┌─────────────────────────────────────────┐
│        UrbanHub - Microservices         │
├─────────────────────────────────────────┤
│ MS Alerte | MS Analyse | MS Autre...    │
│     └──→ RabbitMQ (logs_queue)          │
│          └──→ MS Journalisation         │
│               ├─→ Validation            │
│               ├─→ Persistance (DB)      │
│               └─→ API REST              │
└─────────────────────────────────────────┘
```

### Communication inter-services

#### Envoi de logs par un microservice

Chaque microservice envoie un message JSON sur la queue RabbitMQ `logs_queue` :

```json
{
  "service": "MS Alerte",
  "event_type": "notification_sent",
  "message": "Email envoyé avec succès",
  "level": "INFO",
  "timestamp": "2026-04-21T10:00:00",
  "metadata": {
    "user_id": "123",
    "context": "system"
  }
}
```

#### Récupération des logs

Chaque microservice consulte les logs via l'API REST :

```bash
# Tous les logs
GET /logs

# Logs d'un service
GET /logs/service/{service}

# Logs d'un niveau
GET /logs/level/{level}

# Logs d'erreur
GET /logs/errors
```

### Dépendances UrbanHub

- **RabbitMQ (urbanhub-rabbitmq)** : infrastructure de messagerie partagée
- **PostgreSQL (urbanhub-db)** : base de données centralisée
- **MongoDB (urbanhub-mongodb)** : optionnel, pour stockage alternatif des métadonnées

### Configuration Docker Compose

MS Journalisation s'exécute dans le contexte de `docker-compose.yml` racine :

```bash
# Démarrer tous les services UrbanHub
docker-compose up -d

# Vérifier l'état
docker-compose ps

# Logs du microservice
docker-compose logs ms-journalisation -f
```

### Déploiement dans UrbanHub

1. Build l'image Docker
   ```bash
   bash ms-journalisation/scripts/build.sh
   ```

2. Pousse vers le registre
   ```bash
   REGISTRY=registry.urbanhub.local bash ms-journalisation/scripts/deploy.sh
   ```

3. Met à jour le `docker-compose.yml` UrbanHub
   ```yaml
   ms-journalisation:
     image: registry.urbanhub.local/ms-journalisation:latest
     container_name: urbanhub-journalisation
     ports:
       - "8000:8000"
     environment:
       RABBITMQ_URL: amqp://user:password@urbanhub-rabbitmq:5672
       DATABASE_URL: postgresql://user:password@urbanhub-db:5432/logs
   ```

---

## Résumé

| Section | Contenu clé |
|---------|------------|
| Vue d'ensemble | Architecture hexagonale, flux de données centralisé |
| Étapes | 5 étapes CI/CD : tests, SonarQube, Snyk, upload artefacts |
| Outils | Python 3.12, pytest, SonarQube, Snyk, Docker |
| Prérequis | Python 3.12, secrets GitHub, RabbitMQ optionnel |
| Qualité/Dette | 80%+ couverture, 0 bugs critiques, maintenance régulière |
| Intégration UrbanHub | Logging centralisé, queue RabbitMQ, API REST commune |

---

**Dernière mise à jour** : 26 avril 2026
