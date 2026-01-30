# 🍷 Home Assistant Wine Cellar Manager (AI Powered)

Ce projet transforme votre instance Home Assistant en un gestionnaire de cave intelligent. Il utilise l'IA pour identifier vos bouteilles, générer des fiches techniques complètes et suivre votre inventaire de manière dynamique, sans aucun module complémentaire tiers.

## ✨ Fonctionnalités

* **Identification par IA** : À partir du nom, de la couleur et de l'année, le système interroge Google Gemini. L'IA agit comme un sommelier expert en croisant des sources fiables (Vivino, Wine-Searcher, fiches domaines, etc.).
* **Fiches techniques exhaustives** :
    * **Identité** : Nom exact, Millésime, Couleur, Appellation, Provenance (Région/Pays), Cépages.
    * **Conservation** : Garde conseillée, Année d'apogée, Date limite de consommation, Fenêtre de dégustation.
    * **Expertise** : Note moyenne (avec sources) et Prix moyen constaté.
* **Indicateurs de Confiance** : Chaque donnée affiche par des icones un score de fiabilité lié à la crédibilité des données obtenues par l'IA:
    * ✅ : Très haute (>95%)
    * 🟢 : Haute (>90%)
    * 🟡 : Moyenne (>80%)
    * 🟠 : Faible (>60%)
    * 🔴 : Très incertain
* **Indicateurs d'Apogée** : Un indicateur visuel permet de savoir immédiatement si le vin est en train de maturer, décliner, ou s'il est à son apogée.
    * ⏳ : **À garder** (le vin est trop jeune).
    * 💎 : **Prêt à boire** (dans sa fenêtre optimale).
    * 🍂 : **À boire rapidement** (proche ou passé la date limite).
* **Gestion de Stock** : Ajout en un clic depuis la recherche, boutons +1 / -1 et suppression simplifiée.
* **Statistiques** : Calcul automatique du nombre total de bouteilles en stock et de la valeur estimée de la cave.

* **UPDATE 1** : Facultatif - Un module de visualisation et rangement de cave a été ajouté, ce n'est que du frontend, indépendant du package précédent (hormis les données qu'il récupère du supersensor en lecture). Voir dans la partie BONUS plus bas son fonctionnement et son installation.

* **UPDATE 2** : Un module de conseil d'accord mets et vins par l'IA a été ajouté, qui propose en fonction du repas entré dans un champs texte, le vin le plus pertinent de votre cave, en tenant compte de sa maturité et de son profil. Une explication du choix et des conseils de service sont proposés. Une carte du top 5 des priorités à boire est également fournie sur la base de leur année d'apogée.

* **UPDATE 3** : Un module de conseil d'achat par l'IA a été ajouté, qui propose de compléter sa cave avec des vins complémentaires de ceux de la base de données de l'utilisateur, en termes de styles et de périodes de maturation. Il permet d'entrer un prix maximal et une région privilégiée a choisir dans une liste déroulante.



## 🛠 Prérequis

1.  **Clé API Google Gemini** : Version gratuite ou non (limite d'usage généreuse), à créer sur [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  **Intégration Google Generative AI** : Intégration **native** de Home Assistant.
    * *Configuration* : Si demandé à l'installation (je n'en suis pas convaincu) nommez l'entité de l'action : `google_ai_task`.
4.  **Logs Système** : L'intégration `system_log` doit être active (présente par défaut) pour permettre la remontée des erreurs de quota ou de connexion de l'IA.

## 🚀 Installation

### 1. Organisation des fichiers
* Créez un dossier `packages/` dans votre répertoire de configuration Home Assistant (où se trouve `configuration.yaml`).
* Placez le fichier `gestion_cave.yaml` dans ce dossier `packages/`.

### 2. Configuration du `configuration.yaml`
Ajoutez les lignes suivantes pour activer le système et protéger votre base de données contre le gonflement inutile (l'IA est gourmande en log...) :

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

### 4. Installation des nouvelles fonctions

Pour la partie visualisation et rangement de la cave, voir ci-dessous.

Pour la partie Accords mets et vins et Conseil d'achat, le package `gestion_cave.yaml` a été modifié pour prendre en compte les nouvelles entités et automations, il suffit de remplacer dans le dossier `/packages` le précédent (si vous aviez deja installé une version), puis de relancer votre configuration yaml complète dans les outils de développement pour créer les nouveaux éléments.

Ensuite, copiez le contenu des 3 fichiers cartes (`carte_priorites_apogees.yaml`, `carte_conseil_sommelier.yaml`, `carte_conseil_achats.yaml`) dans 3 cartes différentes de votre dashboard de cave (copier/coller le contenu dans 3 cartes manuelles, ce sont des piles verricales).


## 📖 Utilisation

1. **Saisie** : Tapez le nom, la couleur et l'année dans l'interface du dashboard. Cliquez sur **Rechercher le vin**.
2. **Analyse** : Pendant que l'IA travaille, vous pouvez observer que la demande est bien prise en compte avec un indicateur d'opération. La requête prend environ 10s.
3. **Stockage** : Quand la recherche est terminée, le vin trouvé est décrit sommairement. Si sa description correspond à l'attendu, cliquez sur **Ajouter le vin à la cave** pour basculer le vin de la recherche vers votre inventaire permanent.
4. **Gestion** : Déployez "Afficher la gestion de la cave" pour ajuster vos stocks, à l'aide de la liste déroulante et des boutons associés.
5. **Conseils du sommelier** : Entrez votre repas dans le champs texte et lancez la recherche IA. La réponse arrivera sous 15s. Idem pour les conseils d'achats, les champs sont suffisamment explicites !

----------------------------

# BONUS : Visualisation de la cave à vin et rangement

<img width="725" height="580" alt="image" src="https://github.com/user-attachments/assets/6f794bbb-56c6-4faa-93e2-37d1c2b1f19a" />


J'ai ajouté une interface de visualisation et de rangement de la cave en lien avec le stock de bouteilles de la première page, qui permet de configurer la taille de sa cave et d'y ranger les bouteilles selon leur position physique réelle. 

## 🌟 Fonctions principales
* **Visualisation** : Rendu HTML des bouteilles avec codes couleurs (Rouge, Blanc, Rose).
* **Mode Manuel** : Placement précis bouteille par bouteille via listes déroulantes.
* **Mode Automatique** : Remplissage auto groupant les bouteilles par couleur pour un rendu uniquemnt esthétique.
* **Monitoring** : Comparaison en direct entre l'inventaire du supersensor et les bouteilles rangées de la visualisation, afin d'alerter sur des bouteilles non rangées ou consommées.

## ⚙️ Fonctionnement utilisateur
1.  **Inventaire** : Vos vins sont déclarés dans le `sensor.cave_a_vin_supersensor` de la partie "sommelier IA" du projet. Un cadre markdown détaille les bouteilles non rangées ou en trop dans la visualisation en synchronisation avec le supersensor.
2.  **Dimensionnement de la cave** : Des sliders permettent de définir les lignes et colonnes de la visu de la cave.
3.  **Rangement** : 2 modes de rangement : manuel et auto
    * **Manuel** : Choisissez un vin dans la liste et une coordonnée (ex: `1-2`). Le script met à jour `cave_plan.json` et régénère l'affichage (à mettre à jour avec le bouton de la visu).
    * **Automatique** : Des boutons permettent de vider la cave et de replacer tout le stock disponible en triant par couleur.
4.  **Visualisation** : Une carte Iframe affiche le fichier HTML généré. Un bouton "Actualiser" est intégré au visuel pour le rafraîchissement (2 clicks peuvent être nécessaires...).



## 📂 Arborescence & Installation

Copier les fichiers mis à disposition dans le dossier visualisation du github selon l'arborescence décrite ci-dessous.

### 1. Création des répertoires
Créez les dossiers suivants dans votre répertoire `/config/` (c'est la racine de HA dans File Editor, la ou se trouve le configuration.yaml) :
* `/config/python_scripts/` (moteurs de calcul)
* `/config/packages/` (configuration YAML)
* `/config/www/cave/` (stockage du rendu HTML)

### 2. Emplacement des fichiers
| Fichier | Emplacement | Rôle |
| :--- | :--- | :--- |
| `cave_plan.json` | `/config/` | Base de données des emplacements |
| `generate_cave.py` | `/config/` | Générateur du rendu HTML |
| `cave_management.yaml` | `/config/packages/` | Configuration HA (Sensors, Scripts) |
| `analyze_stock.py` | `/config/python_scripts/` | Calcul des écarts de stock |
| `ranger_vin.py` | `/config/python_scripts/` | Script de rangement manuel |
| `autofill_cave.py` | `/config/python_scripts/` | Script de rangement automatique |
| `empty_cave.py` | `/config/python_scripts/` | Script de vidage complet |
| `mon_casier.html` (généré auto) | `/config/www/cave/` | Fichier de rendu final |

### 3. Configuration du Token API
Vous devez insérer un **TOKEN HA longue durée** dans la variable `TOKEN = "..."` située au début des fichiers suivants :
* `generate_cave.py`
* `python_scripts/autofill_cave.py`
* `python_scripts/empty_cave.py`
* `python_scripts/analyze_stock.py`

Pour créer un jeton longue durée, cliquez sur votre nom en bas du menu à gauche dans HA => onglet Securité => (en bas) Jetons d'accès longue durée / créer un jeton.

## 🚀 Mise en service
1.  **Installation** : Copiez les fichiers dans l'arborescence créée avec Fil Editor, remplissez votre TOKEN longue durée dans les 4 .py et redémarrez Home Assistant pour charger le package.
2.  **Dashboard** : Copiez le contenu du fichier carte_visu.yaml dans une carte manuelle sur votre dashboard (dans une autre page que le sommelier IA pour na pas trop charger le dashboard)
3.  **Initialisation** :
    * Lancez les 2 automatisations `cave_sync_liste_cases' et 'cave_sync_liste_vins` dans le menu des automatisations afin de peupler les listes du dashboard.
    * Lancez le script `script.cave_vidage_complet` dans l'onglet Actions du menu Outils de développement pour créer le fichier plan initial.
4.  **Premier Rendu** : Cliquez sur **"Forcer Visuel"** dans votre interface pour générer le fichier HTML.
5.  **Ajustage** : Si le bas de la cave est coupé dans l'Iframe, augmentez la valeur `aspect_ratio` (ex: `150%`) dans la configuration de votre carte Lovelace.
