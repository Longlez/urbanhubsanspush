# Scripts de build / test / déploiement

Ce dossier contient des scripts versionnés pour les opérations CI/CD du microservice `ms-journalisation`.

## Scripts disponibles

- `build.sh` : installe les dépendances Python et construit l'image Docker `ms-journalisation:ci`
- `test.sh` : installe les dépendances Python et exécute les tests unitaires avec couverture
- `report.sh` : exécute `pytest`, génère `rapport_tests.txt`, `rapport_tests.xml`, `coverage.xml` et la sortie HTML dans `coverage_html/`
- `deploy.sh` : tagge et pousse l'image Docker vers un registre externe, en utilisant `REGISTRY`
- `ci_tools.py` : outil Python multi-commandes pour exécuter `build`, `test`, `report` ou `deploy`

## Exemples d'utilisation

```bash
bash ms-journalisation/scripts/build.sh
bash ms-journalisation/scripts/test.sh
bash ms-journalisation/scripts/report.sh
REGISTRY=myregistry.example.com bash ms-journalisation/scripts/deploy.sh
```

```bash
python ms-journalisation/scripts/ci_tools.py build --image ms-journalisation:ci
python ms-journalisation/scripts/ci_tools.py test
python ms-journalisation/scripts/ci_tools.py report
python ms-journalisation/scripts/ci_tools.py deploy --registry myregistry.example.com
```
