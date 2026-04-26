# UrbanHub - Projet Microservices

# Projet Fil Rouge BC03 Partie 1

---

## Vue d'ensemble

UrbanHub est une plateforme intelligente de supervision urbaine destinée aux autorités locales.
Elle repose sur la collecte et l’analyse de données issues de capteurs IoT (trafic, qualité de l’air, état des infrastructures) afin de fournir une aide à la décision en temps quasi réel.

---

## Architecture

API Gateway → Microservices → RabbitMQ → Bases de données (SQL & MongoDB)

---

## Microservices

- ms-alerte-usager : gestion des alertes  
- ms-analyse : analyse des données  
- ms-collecte-iot : collecte IoT  
- ms-journalisation : centralisation des logs  

---

## Déploiement

docker-compose build  
docker-compose up -d  

---

## Tests et qualité

Outils utilisés :
- pytest
- coverage
- flake8
- SonarQube
- Snyk

---

## Pipeline CI/CD

Pipeline GitHub Actions avec :
- tests automatiques
- analyse de qualité
- scan de sécurité

---

## Déclaration d’utilisation d’IA

### Outils utilisés
- ChatGPT
- GitHub Copilot

### Parties concernées
- Tests unitaires
- Pipeline CI/CD
- Documentation
- Docker

### Exemples de prompts
- "Crée un script de tests avec pytest pour ce projet"
- "Fais une mise en place d'un Workflow GitHub Actions microservices"
- "Crée la partie Dockerfile du projet"

---

## Technologies

Python, FastAPI, MongoDB, SQLAlchemy, RabbitMQ, Docker, GitHub Actions

---

## Installation

git clone <repo>  
pip install -r requirements.txt  

---

## Contributeur

Étudiant : MI202623

---
