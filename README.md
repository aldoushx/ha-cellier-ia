# Gestionnaire de Cellier Intelligent (Gemini)

Ce package pour Home Assistant permet de gérer un inventaire de 20 bouteilles de vin. Il automatise l'enrichissement des données via l'intelligence artificielle Gemini (Google Generative AI) pour fournir des détails œnologiques précis à partir d'une saisie simplifiée.

## Fonctionnement général

Le système fonctionne par un cycle de requêtage et de dispatching :

1. **Saisie** : L'utilisateur renseigne le nom, le millésime et la couleur.
2. **Traitement Gemini** : Le modèle Gemini Pro analyse la saisie pour identifier précisément le vin.
3. **Dispatch** : Une automatisation traite la réponse JSON. Elle met à jour la quantité si le vin existe déjà ou l'inscrit dans le premier emplacement disponible.

## Données stockées (Attributes)

Chaque capteur sensor.vin_1 à sensor.vin_20 contient, en plus de son état principal, les attributs suivants récupérés par l'IA :

* **Informations produit** : Nom complet du domaine, appellation précise, millésime et couleur de la robe.
* **Profil technique** : Liste des cépages et caractéristiques de dégustation.
* **Indice de confiance** : Note de 0 à 100 indiquant le degré de certitude de l'IA sur l'identification du vin.
* **Gestion de cave** : Conseil de garde, fenêtre de consommation optimale et apogée.
* **Évaluation et marché** : Note moyenne calculée et prix moyen constaté.
* **Sources** : Liste des sites spécialisés (magasins, guides, sites de critiques) consultés par Gemini pour compiler ces informations.

## Prérequis

Pour utiliser ce package, les éléments suivants doivent être configurés dans Home Assistant :

1. **Intégration Google Generative AI** :
* Disposer d'une clé API Google AI Studio.
* Installer et configurer l'intégration officielle Google Generative AI.
* Nommer l'entité de service de manière à ce qu'elle soit exploitable par les automatisations du package.


2. **Configuration des Dossiers** :
* Le support des packages doit être activé dans votre fichier configuration.yaml.



## Contenu du package

### Entités de contrôle

* **Saisie** : Entités input_text pour le nom, l'année et la couleur.
* **Retrait** : Un input_select dynamique pour choisir une bouteille à sortir du stock.
* **Déclencheur** : Un input_button qui lance la séquence de recherche Gemini.

### Logique et Automatisation

* **Recherche IA** : Script envoyant le prompt structuré à Gemini et réceptionnant la réponse JSON.
* **Dispatching** : Logique YAML traitant l'attribution des emplacements et la gestion des doublons (Nom + Année + Couleur).
* **Maintenance** : Scripts de réinitialisation des capteurs lors du retrait d'une bouteille (remise à l'état Vide et effacement des attributs).

## Installation

1. Copier le fichier cellier_ia.yaml dans votre répertoire packages.
2. Vérifier que les noms d'entités Gemini dans le fichier correspondent à votre configuration.
3. Recharger la configuration YAML ou redémarrer Home Assistant.
