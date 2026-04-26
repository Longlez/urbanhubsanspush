# L4 — Rapport SonarQube + Snyk

## 1. Contexte

Ce projet intègre déjà SonarQube et Snyk dans le workflow GitHub Actions de `ms-journalisation`.

- Workflow : `.github/workflows/workflow.yml`
- Secrets GitHub requis :
  - `SONAR_HOST_URL`
  - `SONAR_TOKEN`
  - `SNYK_TOKEN`

## 2. Export SonarQube

### Configuration existante

Le workflow exécute :

```yaml
- name: Run SonarQube analysis
  uses: SonarSource/sonarqube-scan-action@v6
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
    SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
  with:
    projectBaseDir: .
    extraArgs: >
      -Dsonar.projectKey=ms-journalisation
      -Dsonar.sources=src
      -Dsonar.python.version=3.12
```

### Export attendu

SonarQube fournit :

- résultats de la qualité du code
- mesures sur les bugs, vulnérabilités et code smells
- qualité de la couverture du code

> Pour exporter les résultats depuis l’IDE, utilisez l’extension SonarLint / SonarQube et connectez-la au serveur via `SONAR_HOST_URL` et `SONAR_TOKEN`.

## 3. Export Snyk

### Configuration existante

Le workflow exécute :

```yaml
- name: Run Snyk security scan
  uses: snyk/actions/python@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
  with:
    args: test --file=requirements.txt --severity-threshold=high --all-projects
```

### Export attendu

Snyk fournit :

- liste des vulnérabilités de dépendances
- classification par sévérité
- suggestions de correction

> Dans VS Code, utilisez l’extension Snyk pour voir les vulnérabilités directement dans l’éditeur et exporter les résultats.

## 4. Interprétation synthétique

### SonarQube

- **Faible** : aucun défaut bloquant / critique, seulement quelques `code smells` mineurs. Le projet est globalement propre.
- **Modéré** : présence de vulnérabilités de sécurité ou de bugs de gravité moyenne, ou plusieurs `code smells` nécessitant correction.
- **Critique** : défauts bloquants ou critiques, vulnérabilités ou bugs importants, couverture insuffisante.

### Snyk

- **Faible** : uniquement des vulnérabilités `low` / `medium` dans des dépendances de développement, aucun `high` ou `critical`.
- **Modéré** : présence de 1-2 vulnérabilités `high`, ou plusieurs `medium` actives dans la production.
- **Critique** : vulnérabilités `critical` ou un grand nombre de vulnérabilités `high` affectant le runtime.

## 5. Exemple de synthèse à produire

- SonarQube : `Faible` si la qualité du code est bonne et si aucun défaut critique n’est trouvé.
- Snyk : `Modéré` si des vulnérabilités `high` existent mais peuvent être corrigées par mise à jour de dépendances.

## 6. Résultats réels

À ce stade, l’environnement de scan n’est pas authentifié pour Snyk depuis l’outil de validation :

- `snyk_code_scan` a échoué avec `User not authenticated. Please run 'snyk_auth' first.`

L’export SonarQube ne peut pas être généré sans un serveur SonarQube accessible et les secrets de connexion.

## 7. Reproduire le rapport

1. Ajouter les secrets GitHub : `SONAR_HOST_URL`, `SONAR_TOKEN`, `SNYK_TOKEN`.
2. Lancer le pipeline sur `main` ou `develop`.
3. Collecter les artefacts générés par GitHub Actions.
4. Ouvrir le rapport `coverage_html/index.html` pour l’inspection locale.

## 8. Remarques pour l’IDE

- Installez `SonarLint` et `Snyk` dans VS Code.
- Configurez SonarLint pour se connecter à `SONAR_HOST_URL` + `SONAR_TOKEN`.
- Connectez Snyk avec votre token `SNYK_TOKEN`.
- Inspectez les résultats directement dans l’arborescence de fichiers.

---

### Conclusion

Le livrable L4 est documenté avec les exports SonarQube et Snyk attendus, ainsi que les interprétations `faible/modéré/critique`. Pour obtenir les données réelles, il suffit d’exécuter le workflow après configuration des secrets et de lancer les extensions IDE correspondantes.
