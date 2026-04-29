# Description du pipeline CI/CD

Le pipeline CI/CD pour `ms6-validateur-capteur` est automatisé via GitHub Actions et comprend quatre étapes principales : tests, qualité du code, sécurité, et construction. Chaque étape dépend de la précédente pour assurer une progression contrôlée.

## Job 1 : Tests (test)

Cette étape exécute la suite de tests unitaires et d'intégration pour valider le comportement du code.

- **Environnement** : Ubuntu latest avec Python 3.12
- **Actions** :
  - Installation des dépendances depuis `requirements.txt` et `requirements-dev.txt`
  - Exécution de pytest pour lancer tous les tests
  - Génération du rapport de couverture
  - Upload de l'artefact de couverture pour analyse ultérieure

Si les tests échouent, le pipeline s'arrête immédiatement, empêchant le déploiement de code défaillant.

## Job 2 : Qualité du code (quality)

Après validation des tests, cette étape vérifie la conformité du code aux standards de qualité.

- **Dépendances** : Nécessite le succès du job de tests
- **Actions** :
  - Installation des outils de développement (flake8)
  - Analyse statique du code avec flake8 selon la configuration `.flake8`
  - Vérification des règles de style et des erreurs potentielles

Cette étape garantit que le code respecte les conventions de l'équipe et reste maintenable.

## Job 3 : Sécurité (security)

L'étape de sécurité scanne les dépendances pour détecter les vulnérabilités connues.

- **Dépendances** : Nécessite le succès du job de qualité
- **Actions** :
  - Utilisation de Snyk pour analyser `requirements.txt`
  - Seuil de sévérité configuré sur "high"
  - Échec du pipeline si des vulnérabilités critiques sont trouvées

Cette protection précoce contre les failles de sécurité est cruciale pour un système urbain sensible.

## Job 4 : Construction (build)

La dernière étape principale construit et valide l'image Docker du microservice.

- **Dépendances** : Nécessite le succès du job de sécurité
- **Actions** :
  - Construction de l'image Docker `ms6-validateur-capteur:ci`
  - Validation basique que l'image se construit sans erreur

Des jobs supplémentaires (verify-image, deploy-staging) complètent le pipeline pour tester l'image et déployer en staging, mais ces quatre jobs forment le cœur de la validation continue.