import json, urllib.request, os

TOKEN = "VOTRE_TOKEN_ICI"
URL_BASE = "http://localhost:8123/api/states/"
PATH_PLAN = "/config/cave_plan.json"

def get_ha(eid):
    req = urllib.request.Request(URL_BASE + eid)
    req.add_header('Authorization', f'Bearer {TOKEN}')
    with urllib.request.urlopen(req) as r: return json.loads(r.read().decode())

try:
    inv = get_ha("sensor.cave_a_vin_supersensor")
    l = int(float(get_ha("input_number.cave_nb_lignes")['state']))
    c = int(float(get_ha("input_number.cave_nb_colonnes")['state']))
    
    vins = inv.get('attributes', {}).get('vins', {})
    stock = []
    for k, v in vins.items():
        nom = f"{v.get('nom',{}).get('valeur','')} {v.get('annee',{}).get('valeur','')}".strip()
        coul = v.get('couleur', {}).get('valeur', 'Rouge').lower()
        for _ in range(int(v.get('nombre_bouteilles', 0))):
            stock.append({"nom": nom, "coul": coul})

    # Tri par couleur (pour grouper les vins visuellement)
    stock.sort(key=lambda x: x['coul'])

    nouveau_plan = {}
    idx = 0
    for row in range(1, l + 1):
        for col in range(1, c + 1):
            cid = f"{row}-{col}"
            nouveau_plan[cid] = stock[idx]['nom'] if idx < len(stock) else "none"
            idx += 1

    with open(PATH_PLAN, 'w', encoding='utf-8') as f:
        json.dump(nouveau_plan, f, indent=4, ensure_ascii=False)
except Exception as e: print(f"Erreur: {e}")
