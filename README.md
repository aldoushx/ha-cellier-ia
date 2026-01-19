# Gestionnaire de Cave à vin pour Home Assistant (avec expertise vin Gemini)

Ce package pour Home Assistant permet de gérer un inventaire de 20 emplacements de vins différents. Il récupère les données du vin sur les sites spécialisés automatiquement par un prompt IA (Gemini) pour mettre à disposition des détails œnologiques précis à partir d'une saisie simplifiée (et tolerante, merci au LLM) sur un dashboard de saisie et d'inventaire.

Le dashboard comporte un binary sensor qui permet de dérouler l'interface de saisie des vins et de gestion des emplacements.

## Fonctionnement général

1. **Saisie** : L'utilisateur renseigne le nom, le millésime et la couleur de son vin.
2. **Traitement Gemini** : Gemini analyse la saisie pour identifier précisément le vin, récupère les infos demandées sur les sites spécialisés et renvoie un JSON. La réponse à la requête met environ 15 secondes à revenir.
3. **Dispatch** : Une automatisation traite le JSON en stockant les infos dans un sensor et remplit les emplacements de la cave de manière intelligente (choisit les emplacements vides, ne duplique pas les vins). Une liste déroulante permet d'effacer les emplacements (un deuxième bouton permet une réinitialisation de la cave, il faut appuyer sur ce bouton avant une première saisie pour initialiser).

Du fait du délai de traitement de la requête par Gemini, il se passe une dizaine de secondes entre l'appui sur le bouton de recherche du vin et le remplissage de l'emplacement de la cave.
La requête échouera en cas d'épuisement du quotat du plan de facturation Gemini (gratuit de mon côté). Le message d'erreur est visible dans Système => Journal avec cette info, et une notification persistante est générée. Si un emplacement cave a été rempli de manière erronée, le vider avec le bouton du dashboard et retenter plus tard. 

## Données stockées (Attributes)

Chaque capteur sensor.vin_1 à sensor.vin_20 contient les attributs suivants récupérés par l'IA :

* **Informations produit** : Nom complet du domaine, appellation précise, millésime et couleur.
* **Cepages** : Liste des cépages.
* **Gestion** : Conseil de garde, fenêtre de consommation et apogée.
* **Évaluation et marché** : Note moyenne des sites spécialisés et prix moyen constaté.
* **Sources** : Liste des sites spécialisés (magasins, guides, sites de critiques) consultés par Gemini pour compiler les informations.
* **Indice de confiance** : Note de 0 à 100 indiquant le degré de certitude de l'IA sur l'identification du vin et les différents attributs.

## Affichage et Code Couleur de Confiance

L'interface du dashboard utilise un système de retour visuel dynamique pour évaluer la fiabilité des informations extraites par Gemini. Chaque donnée clé (Note, Prix, Garde, Apogée) est associée à un attribut `confiance` qui détermine sa couleur d'affichage selon les seuils de certitude de l'IA :

* 🟢 **Vert vif/fluo (#00FF00)** : Confiance absolue (≥ 95%).
* 🟢 **Vert foncé (#4CAF50)** : Fiabilité excellente (90-94%).
* 🟡 **Jaune-Vert (#CDDC39)** : Fiabilité bonne (80-89%).
* 🟠 **Orange (#FF9800)** : Fiabilité modérée (60-79%).
* 🔴 **Rouge (#F44336)** : Fiabilité faible (< 60%), une vérification manuelle est conseillée.

Chaque carte d'emplacement intègre une pastille de couleur située devant le nom du vin, facilitant la lecture rapide de l'inventaire de la cave.
Les informations principales du vin sont affichées sur cette carte, les autres infos sont disponibles en attributs des sensor.vin_xx.

Un autre indicateur est placé devant le nom du vin, qui indique la maturité du vin pour la consommation, à savoir :
* ⏳  **Bonification** : Le vin n'a pas encore atteint son potentiel. À laisser vieillir. 
* 💎  **Apogée** : Fenêtre de dégustation idéale. Le vin est à son sommet.
* 🍂  **Déclin** : L'apogée est dépassée. À consommer en priorité pour éviter la perte. 

## Prérequis

Pour utiliser ce package, les éléments suivants doivent être configurés dans Home Assistant :

1. **Intégration Google Generative AI** :
* Disposer d'une clé API Google AI Studio :
  https://aistudio.google.com/app/apikey?hl=fr
* Installer et configurer l'intégration officielle Google Generative AI.


Nota : pas de paiement requis, le plan gratuit suffit, mais il faudra attendre le temps nécessaire à chaque épuisement du quotat pour compléter sa cave.

2. **Configuration du dossier package de HA** :
* Le support des packages doit être activé dans votre fichier configuration.yaml :

```yaml
homeassistant:
  packages: !include_dir_named packages
```

3. **Configuration de l'accès au log HA** :
* L'accès au journal d'erreur doit être activé dans votre fichier configuration.yaml pour obtenir la notification de quotat IA dépassé :

```yaml
system_log:
  fire_event: true
```

## Contenu du package

### Entités

* Entités input_text pour le nom, l'année et la couleur du vin, le stockage du message de quotat atteint.
* Un input_select dynamique pour choisir l'emplacement de bouteille à vider.
* Un input_button qui lance la séquence de recherche Gemini, deux autres pour les RAZ.
* Des template sensors affichent la valeur totale de la cave et le nombre de bouteilles.

### Automatisations

* **Recherche IA** : Script envoyant le prompt structuré à Gemini et réceptionnant la réponse JSON.
* **Dispatching** : Logique traitant l'attribution des emplacements et la gestion des doublons (Nom + Année + Couleur).
* **Maintenance** : Scripts de réinitialisation des capteurs lors de la vidange d'un emplacement (remise à l'état Vide et effacement des attributs).

## Installation

1. Copier le fichier cellier_ia.yaml dans le répertoire /packages avec file editor (ou ssh etc...).
2. Ajouter les commandes de prise en compte du dossier package et de lecture du log dans le fichier configuration.yaml.
3. Redémarrer Home Assistant.
4. Copier le contenu du dashboard dashboard_cellier.yaml dans un nouveau dashboard.
5. Avant de taper la premiere saisie, initialiser tous les emplacements de la cave en appuyant sur le bouton de reinitialisation totale de la cave sur le dashboard.
6. Enjoy (avec modération ?)
