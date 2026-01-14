# Gestionnaire de Cave à vin pour Home Assistant (avec expertise vin Gemini)

Ce package pour Home Assistant est une première mouture qui permet de gérer un inventaire de 20 emplacements de vins différents. Il récupère les données du vin sur les sites spécialisés automatiquement par un prompt IA (Gemini) pour mettre à disposition des détails œnologiques précis à partir d'une saisie simplifiée, à partir d'un dashboard (à améliorer !) de saisie et d'inventaire.

## Fonctionnement général

1. **Saisie** : L'utilisateur renseigne le nom, le millésime et la couleur.
2. **Traitement Gemini** : Le Gemini analyse la saisie pour identifier précisément le vin, récupère les infos sur les sites spécialisés et renvoie un JSON.
3. **Dispatch** : Une automatisation traite le JSON et remplit les emplacements de la cave de manière intelligente (choisit les emplacements vide, ne duplique pas les vins). Une liste déroulante permet d'effacer les emplacements (il faut faire un RAZ avec ce bouton de chaque emplacement avant de les utiliser).

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


2. **Configuration des Dossiers** :
* Le support des packages doit être activé dans votre fichier configuration.yaml :

```yaml
homeassistant:
  packages: !include_dir_named packages



## Contenu du package

### Entités

* **Saisie** : Entités input_text pour le nom, l'année et la couleur du vin.
* **Retrait** : Un input_select dynamique pour choisir l'emplacement de bouteille à vider.
* **Déclencheur** : Un input_button qui lance la séquence de recherche Gemini.

### Automatisations

* **Recherche IA** : Script envoyant le prompt structuré à Gemini et réceptionnant la réponse JSON.
* **Dispatching** : Logique traitant l'attribution des emplacements et la gestion des doublons (Nom + Année + Couleur).
* **Maintenance** : Scripts de réinitialisation des capteurs lors de la vidange d'un emplacement (remise à l'état Vide et effacement des attributs).

## Installation

1. Copier le fichier cellier_ia.yaml dans votre répertoire packages.
2. Copier le contenu du dashboard dashboard_cellier.yaml dans un nouveau dashboard.
3. Redémarrer Home Assistant.
4. Enjoy (avec modération ?)
