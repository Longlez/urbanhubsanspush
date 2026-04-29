# Configurer le CI/CD

Le workflow GitHub Actions du microservice est défini dans `.github/workflows/ms6-validateur-capteur.yml`.

Il exécute les étapes suivantes :

1. Exécution des tests unitaires et génération des rapports.
2. Vérification de la qualité du code avec Flake8.
3. Construction de l'image Docker.
4. Vérification de l'image en local.
5. Déploiement de staging via Docker Compose.
