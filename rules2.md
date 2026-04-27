# Suite à ce projet, on nous a demandé de créer un nouveau microservice: Validateur de données capteur qui sera nommé exactement comme ceci: MS6 - Validateur de données capteur.
Ce microservice a pour rôle: de porte de qualité entre la collecte IoT et le traitement d'événements. Avant qu'une donnée brute capteur soit propagée sur le bus d'évènements, elle doit êtrer validée et classifiée selon des seuils définis.
## Missions:
Le mission est donc: créer ce microservice from scratch, écrire ses test, le dockeriser, configurer son pipeline GitHub Actions complet avec SonarCloud et Snyk, et produire les rapports d'analyse qualité et sécurité - avant et après corrections.
Donc le positionnement dans l'architecture UrbanHub est comme ceci:
Ca vient du CAPTEURS IoT --> Ms Collecte Iot --> Ms Validateur --> Ms Traitement d'évènements 

### Specification:
De plus, ce microservice a une spécification alors il possède une fonctionnalité qui est: il expose un Endpoint POST/validate , il récoit une donnée capteur et retourne sa classification selon les seuils définis.Donc j'aimerais que tu prennes comme exemple le seuil sont je vais mentionné çi déssous:
Comme premier capteur: co2; Seuil modéré: 800 ; Seuil critique: 1000 ; Unité: ppm 
Comme deuxième capteur : temperature; Seuil modéré: 35 ; Seuil critique: 40 ; Unité °C
Comme troisième capteur: noise; Seuil modéré: 70 ; Seuil critique: 85 ; Unité: dB
Comme quatrième capteur: pm25; Seuil modéré: 25 ; Seuil critique: 50 ; Unité: ug/m3



#### Contrat d'interface:
Comme contrat d'interface j'aimerais que vous suiviez cette exemple:
POST/validate - exemples d'entrée sortie
Entrée: {"sensor": "co2","value": 500.}
Cas 1 - Valeur normale (<seuil modéré):
{"valid": true, "level":"normal", "sensor": "co2", "value": 500.0, "threshold": 800, "timestamp": "2026-04-27T09:00:00Z"}
Cas 12 - Valeur modérée (>=seuil modéré, < seuil critique):
{"valid": true, "level":"moderate", "sensor": "co2", "value": 850.0, "threshold": 800, "timestamp": "2026-04-27T09:00:00Z"}
Cas 3 - Valeur critique (>= seuil critique):
{"valid": false, "level":"critical", "sensor": "co2", "value": 1500.0, "threshold": 1000, "timestamp": "2026-04-27T09:00:00Z"}
Cas 4 - Capteur inconnu:
{"valid": false, "level":"unknown", "message": "Capteur non répertorié"}

##### Structure du dossier
Structure du dossier à créer dans le monorepo est comme ceci:
ms6-validateur-capteur/
  |---src/
  |   -----validator.py 	: ca sert à créer logique métier  
  |---tests/
  |   -----test_validator.py    : ca sert à créer tests pytest ( 4 test au minimum )
  |---Dockerfile		: à créer
  |---requierments.txt		: à créer -- versions fixées

 Workflows GitHub Actions:
 .GitHub/workflows/ms6-validateur.yml

##### Service à ajouter dans le docker-compose.yml existant du groupe:
	ms6-validateur:
	 image: ghcr.io/[org]/urbanhub/ms6-validateur:latest
	 ports:["8006:8000"]
	 networks: [urbanhub-network]
	 healthcheck:
	 test: ['CMD','curl','-f','http://localhost:8000/docs']







