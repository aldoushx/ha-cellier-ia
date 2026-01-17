# Gestionnaire de Cave à vin pour Home Assistant (avec expertise vin Gemini)

Ce package pour Home Assistant est une première mouture qui permet de gérer un inventaire de 20 emplacements de vins différents. Il récupère les données du vin sur les sites spécialisés automatiquement par un prompt IA (Gemini) pour mettre à disposition des détails œnologiques précis à partir d'une saisie simplifiée sur un dashboard (à améliorer !) de saisie et d'inventaire.

## Fonctionnement général

1. **Saisie** : L'utilisateur renseigne le nom, le millésime et la couleur.
2. **Traitement Gemini** : Le Gemini analyse la saisie pour identifier précisément le vin, récupère les infos sur les sites spécialisés et renvoie un JSON. la réponse à la requête mais environ 15 secondes à revenir.
3. **Dispatch** : Une automatisation traite le JSON et remplit les emplacements de la cave de manière intelligente (choisit les emplacements vides, ne duplique pas les vins). Une liste déroulante permet d'effacer les emplacements (un deuxième bouton permet une réinitialisation de la cave, il faut appuyer sur ce bouton avant une première saisie).

Du fait du délai de traitement de la requête par Gemini, il se passe une quinzaine de secondes entre l'appui sur le bouton de recherche du vin et le remplissage de l'emplacement de la cave.

## Données stockées (Attributes)

Chaque capteur sensor.vin_1 à sensor.vin_20 contient les attributs suivants récupérés par l'IA :

* **Informations produit** : Nom complet du domaine, appellation précise, millésime et couleur.
* **Profil technique** : Liste des cépages.
* **Gestion de cave** : Conseil de garde, fenêtre de consommation optimale et apogée.
* **Évaluation et marché** : Note moyenne des sites spécialisés et prix moyen constaté.
* **Sources** : Liste des sites spécialisés (magasins, guides, sites de critiques) consultés par Gemini pour compiler les informations.
* **Indice de confiance** : Note de 0 à 100 indiquant le degré de certitude de l'IA sur l'identification du vin et les différents attributs.

## Prérequis

Pour utiliser ce package, les éléments suivants doivent être configurés dans Home Assistant :

1. **Intégration Google Generative AI** :
* Disposer d'une clé API Google AI Studio.
* Installer et configurer l'intégration officielle Google Generative AI.
Nota : pas de paiement requis, le plan gratuit suffit, mais il faudra attendre le temps nécessaire à chaque épuisement des tokens pour compléter sa cave.


2. **Configuration du dossier package de HA** :
* Le support des packages doit être activé dans votre fichier configuration.yaml :

```yaml
homeassistant:
  packages: !include_dir_named packages
```


## Contenu du package

### Entités

* **Saisie** : Entités input_text pour le nom, l'année et la couleur du vin.
* **Retrait** : Un input_select dynamique pour choisir l'emplacement de bouteille à vider.
* **Déclencheur** : Un input_button qui lance la séquence de recherche Gemini.
* ... (a compléter)

### Automatisations

* **Recherche IA** : Script envoyant le prompt structuré à Gemini et réceptionnant la réponse JSON.
* **Dispatching** : Logique traitant l'attribution des emplacements et la gestion des doublons (Nom + Année + Couleur).
* **Maintenance** : Scripts de réinitialisation des capteurs lors de la vidange d'un emplacement (remise à l'état Vide et effacement des attributs).

## Installation

1. Copier le fichier cellier_ia.yaml dans le répertoire packages avec file editor (ou ssh etc...).
2. Copier le contenu du dashboard dashboard_cellier.yaml dans un nouveau dashboard.
3. Redémarrer Home Assistant.
4. Avant de taper la premiere saisie, initialiser tous les emplacements de la cave en appuyant sur le bouton de reinitialisation totale du dashboard.
5. Enjoy (avec modération ?)
