# Présentation du microservice ms6-validateur-capteur

## Vue d'ensemble

Le microservice `ms6-validateur-capteur` fait partie de l'écosystème UrbanHub, un système de gestion urbaine intelligente. Son rôle principal est de valider et classifier les données provenant des capteurs environnementaux déployés dans la ville, ainsi que de traiter les fenêtres de trafic pour enrichir les analyses urbaines.

## Fonctionnalités clés

### Validation des données de capteurs

Le service reçoit des données brutes de capteurs mesurant divers paramètres environnementaux :
- Concentration en CO2
- Température ambiante
- Niveau de bruit
- Humidité relative
- Pression atmosphérique

Pour chaque capteur, il applique des seuils de validation prédéfinis pour déterminer si les valeurs sont dans des plages acceptables ou si elles indiquent des anomalies potentielles.

### Classification des capteurs

En fonction des seuils dépassés, les capteurs sont classifiés selon trois catégories :
- **Valide** : Toutes les mesures sont dans les normes
- **Alerte** : Une ou plusieurs mesures dépassent les seuils d'alerte
- **Critique** : Des mesures critiques indiquent un problème urgent

### Traitement des fenêtres de trafic

Le service gère également les données de trafic urbain, en validant les fenêtres temporelles et en enrichissant les informations avec des métadonnées contextuelles.

## Architecture technique

Le microservice est construit avec FastAPI pour les API REST, utilise Pydantic pour la validation des schémas de données, et s'intègre avec RabbitMQ pour la messagerie asynchrone. Il suit une architecture en couches (adapters, domain, ports) pour une séparation claire des préoccupations.

## Intégration dans UrbanHub

En tant que composant de validation, `ms6-validateur-capteur` joue un rôle crucial dans la chaîne de traitement des données urbaines. Il assure la qualité des informations avant leur transmission aux services d'analyse et de décision.