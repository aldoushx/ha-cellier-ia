# 🍷 Home Assistant Wine Cellar Manager (AI Powered)

Ce projet transforme votre instance Home Assistant en un gestionnaire de cave intelligent. Il utilise l'IA pour identifier vos bouteilles, générer des fiches techniques complètes et suivre votre inventaire de manière dynamique, sans aucun module complémentaire tiers.

## ✨ Fonctionnalités

* **Identification par IA** : À partir du nom, de la couleur et de l'année, le système interroge Google Gemini. L'IA agit comme un sommelier expert en croisant des sources fiables (Vivino, Wine-Searcher, fiches domaines, etc.).
* **Fiches techniques exhaustives** :
    * **Identité** : Nom exact, Millésime, Couleur, Appellation, Provenance (Région/Pays), Cépages.
    * **Conservation** : Garde conseillée, Année d'apogée, Date limite de consommation, Fenêtre de dégustation.
    * **Expertise** : Note moyenne (avec sources) et Prix moyen constaté.
* **Indicateurs de Confiance** : Chaque donnée affiche un score de fiabilité :
    * ✅ : Très haute (>95%)
    * 🟢 : Haute (>90%)
    * 🟡 : Moyenne (>80%)
    * 🟠 : Faible (>60%)
    * 🔴 : Très incertain
* **Indicateurs d'Apogée** : 
    * ⏳ : **À garder** (le vin est trop jeune).
    * 🍷 : **Prêt à boire** (dans sa fenêtre optimale).
    * ⚠️ : **À boire rapidement** (proche ou passé la date limite).
* **Gestion de Stock** : Ajout en un clic depuis la recherche, boutons +1 / -1 et suppression simplifiée.
* **Statistiques** : Calcul automatique du nombre total de bouteilles et de la valeur estimée de la cave.

## 🛠 Prérequis

1.  **Clé API Google Gemini** : Indispensable et gratuite (limite d'usage généreuse) à créer sur [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  **Intégration Google Generative AI** : Intégration **native** de Home Assistant.
3.  **Logs Système** : L'intégration `system_log` doit être active (présente par défaut) pour permettre la remontée des erreurs de quota ou de connexion de l'IA.

## 🚀 Installation

### 1. Organisation des fichiers
* Créez un dossier `packages/` dans votre répertoire de configuration Home Assistant (où se trouve `configuration.yaml`).
* Placez le fichier `gestion_cave.yaml` dans ce dossier `packages/`.

### 2. Configuration du `configuration.yaml`
Ajoutez les lignes suivantes pour activer le système et **protéger votre base de données** contre le gonflement inutile :

```yaml
homeassistant:
  packages: !include_dir_named packages

# Configuration du Recorder pour protéger votre stockage
recorder:
  purge_keep_days: 7
  exclude:
    entities:
      - sensor.vin_recherche # Donnée temporaire volumineuse
      - input_text.derniere_erreur_gemini
    event_types:
      - system_log_event # Évite d'historiser les erreurs système répétitives

```

### 3. Installation du Dashboard

1. Créez une nouvelle vue dans votre tableau de bord.
2. Cliquez sur les trois points (en haut à droite) > **Modifier le tableau de bord**.
3. Cliquez à nouveau sur les trois points > **Éditeur de code**.
4. Copiez et collez le contenu du fichier `dashboard_v2.yaml`.

## 📖 Utilisation

1. **Saisie** : Tapez le nom, la couleur et l'année. Cliquez sur **Lancer IA**.
2. **Analyse** : Observez les indicateurs de confiance. Si l'IA a fait une erreur de lecture JSON, un indicateur d'erreur s'allumera.
3. **Stockage** : Cliquez sur **Ajouter** pour basculer le vin de la recherche vers votre inventaire permanent.
4. **Gestion** : Déployez "Afficher la gestion de la cave" pour ajuster vos stocks.

