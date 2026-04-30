# Évolutivité et intégration UrbanHub

## Positionnement dans l'architecture UrbanHub

Le microservice `ms6-validateur-capteur` s'intègre parfaitement dans UrbanHub en tant que composant de validation et d'enrichissement des données urbaines. Sa conception modulaire permet une évolution indépendante tout en maintenant la cohérence globale du système.

## Capacités d'évolutivité

### Scalabilité horizontale

- **Architecture stateless** : Chaque instance est indépendante, permettant un scaling automatique
- **Load balancing** : Compatible avec Kubernetes et services de load balancing cloud
- **Partitionnement** : Possibilité de traiter différents types de capteurs sur des instances dédiées

### Extension des fonctionnalités

- **Ajout de nouveaux types de capteurs** : Le système de seuils dynamiques permet d'intégrer facilement de nouveaux paramètres
- **Règles de validation personnalisables** : Possibilité d'ajouter des validateurs métier spécifiques
- **Intégrations externes** : Architecture adapter permet l'ajout de nouveaux protocoles (MQTT, Kafka, etc.)

### Performance

- **Traitement asynchrone** : Utilisation de RabbitMQ pour découpler la validation des traitements lourds
- **Cache intelligent** : Possibilité d'implémenter des caches Redis pour les seuils fréquemment utilisés
- **Optimisation mémoire** : Utilisation de Pydantic pour une validation efficace sans surcharge

## Intégration avec les autres microservices

### Flux de données

1. **Réception** : Données brutes des capteurs via API ou message queue
2. **Validation** : Application des règles métier et seuils
3. **Enrichissement** : Ajout de métadonnées contextuelles (localisation, timestamp)
4. **Publication** : Diffusion vers les services consommateurs (analyse, stockage, alertes)

### Interfaces standardisées

- **API REST** : Endpoints documentés avec OpenAPI pour l'intégration
- **Messages RabbitMQ** : Schémas JSON standardisés pour l'échange inter-services
- **Métriques** : Exposition de métriques Prometheus pour le monitoring

## Évolution future

### Roadmap technique

- **Migration vers Python 3.12** : Amélioration des performances et sécurité
- **Adoption de FastAPI 0.100+** : Nouvelles fonctionnalités et corrections de sécurité
- **Intégration Kubernetes** : Déploiement natif cloud avec auto-scaling
- **Observabilité avancée** : Traces distribuées et monitoring métier

### Extensions envisagées

- **Machine Learning** : Intégration de modèles pour la détection d'anomalies
- **IoT Edge** : Déploiement sur appareils de bord pour validation locale
- **API GraphQL** : Interface flexible pour les consommateurs avancés
- **Streaming temps réel** : Traitement de flux continus de données

## Contraintes et limites

### Limites actuelles

- **Volume de données** : Optimisé pour 1000 capteurs simultanés (extensible)
- **Latence** : Validation en <100ms pour maintenir la réactivité
- **Persistance** : Données validées non stockées localement (déléguées)

### Bonne pratiques d'évolution

- **Tests automatisés** : Couverture >80% pour toute nouvelle fonctionnalité
- **Documentation** : Mise à jour systématique de la doc Diátaxis
- **Revue de code** : Validation par les pairs avant merge
- **Déploiement progressif** : Utilisation de feature flags pour les changements majeurs

## Contribution à l'écosystème UrbanHub

En tant que service de validation, `ms6-validateur-capteur` assure la qualité des données qui alimentent tous les autres composants du système urbain. Son évolutivité garantit que UrbanHub peut s'adapter aux besoins croissants d'une ville intelligente en expansion.

## Guides pratiques d'extension

### Comment ajouter un nouveau capteur dans le validateur

Quand on veut intégrer un nouveau type de capteur, comme un détecteur de particules fines PM2.5 ou un capteur de luminosité, voici comment procéder étape par étape :

1. **Définir les seuils dans la configuration** :
   Ouvrez `src/config/sensor_thresholds.py` et ajoutez votre nouveau capteur :
   ```python
   THRESHOLDS = {
       # Capteurs existants...
       "pm25": {"min": 0, "max": 50},  # Nouveau capteur PM2.5
   }
   ```

2. **Mettre à jour la logique de validation** :
   Dans `src/domain/sensor_validation.py`, ajoutez la validation spécifique :
   ```python
   def _validate_pm25(self, sensor_id, value):
       thresholds = self._get_thresholds("pm25")
       if value < thresholds["min"] or value > thresholds["max"]:
           return "alerte"
       return "valide"
   ```

3. **Intégrer dans la méthode principale** :
   Modifiez `validate_sensor()` pour appeler votre nouvelle méthode :
   ```python
   def validate_sensor(self, sensor_id, data):
       # Validations existantes...
       if hasattr(data, 'pm25'):
           status = self._validate_pm25(sensor_id, data.pm25)
           if status != "valide":
               return status
       return "valide"
   ```

4. **Tester avec des données réelles** :
   Lancez `pytest` pour vérifier que vos ajouts ne cassent rien, puis testez avec des données de test.

C'est assez direct une fois qu'on a compris le pattern. Le plus important est de maintenir la cohérence avec les autres validateurs.

### Comment ajouter un nouveau seuil

Pour modifier ou ajouter des seuils de validation, c'est encore plus simple :

1. **Localisation** : Tout se passe dans `src/config/sensor_thresholds.py`

2. **Modification** : Éditez directement le dictionnaire `THRESHOLDS` :
   ```python
   THRESHOLDS = {
       "temperature": {
           "min": 10,    # Seuil actuel
           "max": 35     # Seuil actuel
       }
   }
   ```

3. **Test** : Après modification, relancez les tests pour vérifier que les nouvelles valeurs sont prises en compte.

On a choisi cette approche centralisée parce que ça permet de modifier les seuils sans toucher au code métier. C'est pratique pour l'ajustement fin en production.

## Intégration dans l'infrastructure

### Docker Compose du groupe

Le microservice s'intègre proprement dans le docker-compose.yml du projet UrbanHub :

- **Service ajouté** : `ms6-validateur-capteur` basé sur l'image `ghcr.io/<org>/ms6-validateur-capteur:ci`
- **Port utilisé** : Exposition sur `8006:8000` (port externe 8006, interne 8000)
- **Réseau** : Partage le réseau `urbanhub_default` avec les autres services pour la communication RabbitMQ

Dans le compose, ça ressemble à ça :
```yaml
services:
  ms6-validateur-capteur:
    image: ghcr.io/monorg/urbanhub/ms6-validateur-capteur:ci
    ports:
      - "8006:8000"
    depends_on:
      - rabbitmq
    environment:
      - RABBITMQ_HOST=rabbitmq
```

Cette intégration permet de lancer tout l'écosystème avec un simple `docker compose up` et d'avoir le validateur accessible sur le port 8006.

### Lien avec BC04 - Déploiement Cloud

Pour l'intégration Kubernetes (BC04), ce microservice se déploiera comme un Deployment standard :

- **Image** : Utilisation de l'image GHCR poussée par le pipeline CI
- **Scaling** : HorizontalPodAutoscaler basé sur la CPU/mémoire
- **Service** : ClusterIP pour l'accès interne, LoadBalancer pour l'exposition externe si nécessaire
- **ConfigMaps** : Seuils de capteurs injectés via ConfigMap pour modification sans rebuild
- **Secrets** : RabbitMQ credentials via Kubernetes secrets

Dans le manifest Kubernetes, on aura quelque chose comme :
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ms6-validateur-capteur
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: validator
        image: ghcr.io/monorg/urbanhub/ms6-validateur-capteur:v1.0.0
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: sensor-thresholds
        - secretRef:
            name: rabbitmq-secret
```

L'avantage de cette approche, c'est que le service peut scaler automatiquement selon la charge, et les mises à jour se font via rolling updates sans interruption.

## Pistes d'amélioration pour les versions futures

En travaillant sur ce microservice, plusieurs idées d'amélioration se sont dégagées naturellement :

### Performance et scalabilité
- **Cache Redis** : Pour les seuils fréquemment consultés, éviter les accès disque répétés
- **Validation par batch** : Traiter plusieurs capteurs en une seule requête pour réduire la latence réseau
- **Optimisation mémoire** : Les gros payloads JSON pourraient être streamés plutôt que chargés en mémoire

### Fonctionnalités métier
- **Validation temporelle** : Détecter les anomalies sur séries temporelles (valeurs qui dévient soudainement)
- **Machine Learning** : Intégrer des modèles de prédiction d'anomalies basés sur l'historique
- **Alertes intelligentes** : Différencier les alertes critiques des dérives normales

### Observabilité
- **Métriques détaillées** : Nombre de validations par type de capteur, taux d'erreur par endpoint
- **Traces distribuées** : Suivre le chemin complet d'une donnée depuis la réception jusqu'à la publication
- **Dashboards** : Interface web pour visualiser l'état des capteurs en temps réel

### Sécurité
- **Rate limiting** : Protection contre les attaques par déni de service
- **Authentification** : Tokens JWT pour sécuriser les appels API entre services
- **Audit logging** : Traçabilité complète des validations pour conformité RGPD

Ces améliorations viendront naturellement avec l'usage en production et les retours des équipes opérationnelles. Pour l'instant, on a un socle solide qui fonctionne bien.