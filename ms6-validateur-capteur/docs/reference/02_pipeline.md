# Description du pipeline CI/CD

Le pipeline CI/CD pour `ms6-validateur-capteur` est automatisé via GitHub Actions et comprend quatre étapes principales : tests, qualité du code, sécurité, construction, puis déploiement en staging. Chaque étape dépend de la précédente pour assurer une progression contrôlée.

## Job 1 : Tests

Cette étape exécute la suite de tests unitaires et d'intégration pour valider le comportement du code.

- **Environnement** : Ubuntu latest avec Python 3.12
- **Commandes attendues** :
  - `python -m pip install --upgrade pip`
  - `pip install -r requirements.txt`
  - `pip install -r requirements-dev.txt`
  - `pytest`
- **Détails tests** :
  - Les tests sont exécutés sur l'ensemble du code source et de la couche `tests/`
  - Le seuil de couverture est fixé à **80%** ou plus
- **Rapports générés** :
  - `03_rapport_tests/rapport_tests.xml`
  - `03_rapport_tests/coverage.xml`
  - rapport de test au format `txt` si configuré dans le job GitHub Actions
- **Actions** :
  - Installation des dépendances
  - Lancement de pytest
  - Génération du rapport de couverture
  - Upload de l'artefact de couverture pour analyse ultérieure

Si les tests échouent, le pipeline s'arrête immédiatement, ce qui empêche le déploiement de code défaillant.

## Job 2 : Qualité du code (quality)

Après validation des tests, cette étape vérifie la conformité du code aux standards de qualité.

- **Dépendances** : Nécessite le succès du job de tests
- **Commandes attendues** :
  - `python -m pip install --upgrade pip`
  - `pip install -r requirements-dev.txt`
  - `pip install flake8`
  - `flake8 src tests --config=.flake8`
- **Outils et configuration** :
  - `flake8` avec configuration dans `.flake8`
  - Paramètres significatifs : limites de complexité, longueur de ligne, style de code et erreurs de syntaxe
  - Possibilité d’ajouter plus tard `black` ou `isort` pour la mise en forme
- **GitHub Secrets** :
  - Aucun token n’est requis pour `flake8` lui-même
  - Les secrets GitHub sont utilisés pour les étapes de sécurité et publication, mais pas pour la simple analyse de qualité
- **Démarche AVANT/APRÈS** :
  - AVANT : code sans vérification statique, risque de style incohérent et d’erreurs silencieuses
  - APRÈS : validation du code, repérage des défauts, et amélioration de la maintenabilité grâce à des règles explicites

Cette étape garantit que le code respecte les conventions de l'équipe et reste maintenable.

## Job 3 : Sécurité (security)

L'étape de sécurité scanne les dépendances pour détecter les vulnérabilités connues.

- **Dépendances** : Nécessite le succès du job de qualité
- **Commandes attendues** :
  - `python -m pip install --upgrade pip`
  - `pip install -r requirements.txt`
- **Actions** :
  - Utilisation de Snyk pour analyser `requirements.txt`
  - Seuil de sévérité configuré sur `high`
  - Échec du pipeline si des vulnérabilités critiques sont trouvées
- **Tokens et secrets** :
  - `SNYK_TOKEN` dans GitHub Secrets
  - Utilisé pour authentifier le scan et accéder à l’API Snyk
- **Détails attendus** :
  - Rapport de vulnérabilités Snyk en sortie
  - Filtrage sur les problèmes de sévérité "high" et plus

Cette protection précoce contre les failles de sécurité est cruciale pour un système urbain sensible.

## Job 4 : Construction (build)

Cette étape construit et prépare l’image Docker du microservice.

- **Dépendances** : Nécessite le succès du job de sécurité
- **Commandes attendues** :
  - `docker build -t ms6-validateur-capteur:ci ms6-validateur-capteur`
  - `docker push ghcr.io/<organisation>/ms6-validateur-capteur:ci`
- **Convention de nommage** :
  - Image nommée `ghcr.io/<organisation>/ms6-validateur-capteur:<tag>`
  - `<organisation>` remplacée par le nom GitHub de l’organisation
- **Authentification** :
  - `GHCR_TOKEN` dans GitHub Secrets
  - Utilisé pour se connecter à GitHub Container Registry avant le `docker push`
- **Vérification de l’image** :
  - `docker run --rm -d --name ms6-validateur-ci -p 8000:8000 ms6-validateur-capteur:ci`
  - Test de l’endpoint `/health` après démarrage
  - Arrêt et suppression du conteneur après vérification

Cette étape garantit que l’image Docker se construit correctement et est prête pour un usage ultérieur.

## Job 5 : Déploiement en staging (deploy-staging)

Cette étape utilise Docker Compose pour déployer le service en environnement de staging.

- **Dépendances** : Nécessite le succès du job de build et des vérifications
- **Commandes attendues** :
  - `docker compose up -d ms6-validateur-capteur`
  - `curl --fail http://localhost:8006/health`
- **Détails attendus** :
  - Service `ms6-validateur-capteur` défini dans `docker-compose.yml`
  - Port exposé `8006` pour l’accès local
  - Vérification via healthcheck sur `/health`
  - Validation que le service répond correctement après démarrage

Cette étape assure que le déploiement Docker Compose fonctionne et que le microservice est accessible sur le port prévu.

## Job 6: Déclencheurs

Le workflow est configuré pour se lancer automatiquement sur :

- **Branches** : `main`, `develop`
- **Chemins** : `ms6-validateur-capteur/**`
- **Événements** : `push` et `pull_request`
- **Pull request** : uniquement vers `main`

Ces déclencheurs garantissent que seule la partie `ms6-validateur-capteur` du repository active le pipeline, et que les modifications proposées via pull request vers `main` sont vérifiées avant merge.

## Récapitulatif des livrables attendus

- Commandes de tests et d’installation clairement documentées
- Seuil de couverture **80%** enforceable
- Rapports générés en `xml` et `txt` pour les tests
- Détails de configuration des outils de qualité
- Utilisation de tokens GitHub Secrets pour la sécurité et la publication
- Commandes Docker `build`, `push`, `run` et convention `ghcr.io`
- Déploiement `docker-compose` du service sur le port `8006` avec healthcheck

Ces éléments décrivent précisément le pipeline attendu pour `ms6-validateur-capteur`, sans ajouter de fonctionnalités supplémentaires au projet.