import json
import sys
import os

# 1. Récupération des arguments envoyés par la shell_command
# sys.argv[1] est la CASE (ex: 1-1)
# sys.argv[2] est le NOM DU VIN
if len(sys.argv) < 3:
    print("Erreur : Arguments manquants (case et vin requis)")
    sys.exit(1)

case_id = sys.argv[1]
vin_nom = sys.argv[2]
path = "/config/cave_plan.json"

# 2. Chargement du fichier JSON existant
if os.path.exists(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            plan = json.load(f)
    except Exception:
        plan = {}
else:
    plan = {}

# 3. Logique de mise à jour
# Si le vin est "none", on retire l'entrée pour cette case
if vin_nom.lower() == "none":
    if case_id in plan:
        plan.pop(case_id)
        print(f"Case {case_id} vidée.")
else:
    # On utilise la CASE comme clé unique. 
    # Cela permet d'avoir le même vin dans plusieurs cases différentes.
    plan[case_id] = vin_nom
    print(f"Vin '{vin_nom}' placé en case {case_id}.")

# 4. Sauvegarde sécurisée
try:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(plan, f, indent=4, ensure_ascii=False)
except Exception as e:
    print(f"Erreur lors de la sauvegarde : {e}")
    sys.exit(1)
