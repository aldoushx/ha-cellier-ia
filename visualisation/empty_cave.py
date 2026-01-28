import json, urllib.request, os

TOKEN = "VOTRE_TOKEN_ICI"
URL_BASE = "http://localhost:8123/api/states/"
PATH_PLAN = "/config/cave_plan.json"

def get_ha(eid):
    req = urllib.request.Request(URL_BASE + eid)
    req.add_header('Authorization', f'Bearer {TOKEN}')
    with urllib.request.urlopen(req) as r: return json.loads(r.read().decode())

try:
    l = int(float(get_ha("input_number.cave_nb_lignes")['state']))
    c = int(float(get_ha("input_number.cave_nb_colonnes")['state']))
    nouveau_plan = {f"{row}-{col}": "none" for row in range(1, l + 1) for col in range(1, c + 1)}
    with open(PATH_PLAN, 'w', encoding='utf-8') as f:
        json.dump(nouveau_plan, f, indent=4, ensure_ascii=False)
except Exception as e: print(f"Erreur: {e}")
