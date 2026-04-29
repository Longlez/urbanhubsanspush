# Guide de création du GitHub Wiki pour UrbanHub

## Objectif

Ce guide vous accompagne dans la création d'un GitHub Wiki pour le projet UrbanHub, en important la documentation existante et en la structurant de manière accessible pour les utilisateurs et contributeurs.

## Prérequis

- Accès administrateur au repository GitHub UrbanHub
- Documentation prête dans le dossier `docs/` du projet
- Connaissance basique de Markdown et GitHub

## Étape 1 : Accéder au Wiki

1. Ouvrez votre repository GitHub dans un navigateur web
2. Cliquez sur l'onglet **"Wiki"** dans la barre de navigation supérieure
3. Si le Wiki n'est pas encore activé, cliquez sur **"Create the first page"**

## Étape 2 : Configurer la page d'accueil

1. Sur la page de création, donnez un titre : `UrbanHub - Documentation`
2. Dans le contenu, créez une introduction :

```
# UrbanHub Documentation

Bienvenue dans la documentation officielle d'UrbanHub, le système de gestion urbaine intelligente.

## Microservices

- [ms6-validateur-capteur](ms6-validateur-capteur) - Validation et classification des données de capteurs
- [ms-analyse](ms-analyse) - Service d'analyse des données urbaines
- [ms-alerte-usager](ms-alerte-usager) - Gestion des alertes utilisateurs
- [ms-collecte-iot](ms-collecte-iot) - Collecte des données IoT
- [ms-journalisation](ms-journalisation) - Service de journalisation

## Démarrage rapide

Consultez le [Guide de prise en main](Guide-de-prise-en-main) pour commencer.
```

3. Cliquez sur **"Save Page"**

## Étape 3 : Importer la documentation existante

### Méthode 1 : Import manuel (recommandé pour contrôle)

1. Allez dans l'onglet Wiki
2. Cliquez sur **"New Page"**
3. Pour chaque fichier de documentation :

   - Copiez le contenu depuis `docs/explanation/01_presentation.md`
   - Créez une page "Présentation-ms6-validateur-capteur"
   - Répétez pour chaque fichier

### Méthode 2 : Utiliser l'API GitHub (pour automation)

Si vous avez beaucoup de fichiers, vous pouvez utiliser l'API GitHub pour importer automatiquement :

```bash
# Exemple de script pour uploader via API
curl -X PUT \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  https://api.github.com/repos/YOUR_ORG/UrbanHub/wikis/ms6-validateur-capteur \
  -d '{"content": "'"$(cat docs/explanation/01_presentation.md)"'"}'
```

## Étape 4 : Organiser la structure des pages

Créez les pages suivantes en vous basant sur la documentation Diátaxis :

### Section Présentation
- `Home` - Page d'accueil
- `Architecture-globale` - Vue d'ensemble du système

### Section ms6-validateur-capteur
- `ms6-validateur-capteur/Presentation` - Présentation du microservice
- `ms6-validateur-capteur/Pipeline-CI-CD` - Description du pipeline
- `ms6-validateur-capteur/SonarCloud` - Analyse qualité du code
- `ms6-validateur-capteur/Snyk` - Analyse cybersécurité
- `ms6-validateur-capteur/Guide-developpeur` - Prise en main
- `ms6-validateur-capteur/Evolutivite` - Évolutivité et intégration

### Section Guides pratiques
- `Installation-locale` - Guide d'installation
- `Contribuer` - Guide pour contributeurs
- `Deploiement` - Guide de déploiement

### Section Référence technique
- `API-Reference` - Documentation des APIs
- `Schemas-donnees` - Schémas de données
- `Configurations` - Fichiers de configuration

## Étape 5 : Personnaliser l'apparence

1. Allez dans les **"Wiki Settings"** (icône d'engrenage)
2. Configurez :
   - Nom du Wiki : "UrbanHub Documentation"
   - Description : "Documentation technique et guides utilisateur"
   - Activez les commentaires si souhaité

## Étape 6 : Ajouter des liens de navigation

Dans chaque page, ajoutez une barre de navigation en haut :

```
**[← Retour à l'accueil](Home)** | **[Guide suivant →](Guide-suivant)**
```

## Étape 7 : Maintenance et mise à jour

1. **Synchronisation** : Quand la doc locale change, mettez à jour le Wiki
2. **Revue** : Demandez aux équipes de relire les pages importantes
3. **Archivage** : Gardez un historique des versions majeures

## Étape 8 : Créer le fichier lien_wiki.txt

Après avoir créé le Wiki, créez un fichier `lien_wiki.txt` à la racine du repository avec le lien public :

```
https://github.com/VOTRE_ORG/UrbanHub/wiki
```

Remplacez `VOTRE_ORG` par le nom réel de votre organisation GitHub.

## Conseils pour un Wiki réussi

- **Cohérence** : Utilisez la même structure que la doc locale
- **Liens** : Référencez les issues et PRs GitHub quand pertinent
- **Images** : Uploadez des diagrammes depuis `docs/` si nécessaire
- **Recherche** : Le Wiki est indexé par GitHub, facilite la recherche
- **Collaboration** : Autorisez les contributions sur le Wiki si approprié

## Validation finale

- Vérifiez que toutes les pages sont accessibles
- Testez les liens internes
- Assurez-vous que le contenu est à jour
- Partagez le lien avec l'équipe

Ce guide devrait vous permettre de créer un Wiki complet et maintenable pour UrbanHub.