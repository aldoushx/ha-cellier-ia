import json
import urllib.request
import os
import unicodedata

# --- CONFIGURATION ---
TOKEN = "VOTRE_TOKEN_ICI"
URL_BASE = "http://localhost:8123/api/states/"
PATH_PLAN = "/config/cave_plan.json"
PATH_HTML = "/config/www/cave/mon_casier.html"

def slugify(text):
    """ Normalise le texte pour garantir la correspondance (accents, espaces, casse) """
    if not text: return ""
    text = unicodedata.normalize('NFD', str(text)).encode('ascii', 'ignore').decode('utf-8')
    return " ".join(text.lower().split())

def get_ha_state(entity_id):
    """ Récupère les données d'une entité via l'API """
    url = f"{URL_BASE}{entity_id}"
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {TOKEN}')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Erreur API {entity_id}: {e}")
        return None

def generate():
    try:
        # 1. Extraction des données du Sensor et des Dimensions
        data_inv = get_ha_state("sensor.cave_a_vin_supersensor")
        data_l = get_ha_state("input_number.cave_nb_lignes")
        data_c = get_ha_state("input_number.cave_nb_colonnes")
        
        if not data_inv: return

        lignes = int(float(data_l['state'])) if data_l else 10
        colonnes = int(float(data_c['state'])) if data_c else 6

        # 2. Construction du dictionnaire de couleurs
        mapping_couleurs = {}
        vins_dict = data_inv.get('attributes', {}).get('vins', {})
        for key, info in vins_dict.items():
            nom = info.get('nom', {}).get('valeur', '')
            annee = info.get('annee', {}).get('valeur', '')
            coul = str(info.get('couleur', {}).get('valeur', 'rouge')).lower()
            
            cle = slugify(f"{nom} {annee}")
            mapping_couleurs[cle] = coul

        # 3. Chargement du plan de rangement JSON
        if os.path.exists(PATH_PLAN):
            with open(PATH_PLAN, 'r', encoding='utf-8') as f:
                plan = json.load(f)
        else: plan = {}

        # 4. Génération du HTML
        grid_template = f"repeat({colonnes}, 1fr)"
        html = f"""<!DOCTYPE html><html><head><meta charset='UTF-8'>
        <style>
            html, body {{ background: white; margin: 0; padding: 0; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; }}
            .btn-update {{ margin: 10px; background: #222; color: #00d4ff; border: 1px solid #444; padding: 6px 15px; border-radius: 5px; cursor: pointer; font-size: 10px; font-weight: bold; }}
            .fridge-exterior {{ padding: 12px; background: #222; border: 3px solid #3d3d3d; border-radius: 8px; }}
            .rack {{ display: grid; grid-template-columns: {grid_template}; gap: 10px; background: #050505; padding: 15px; }}
            .slot {{ width: 38px; height: 38px; border-radius: 50%; background: #111; display: flex; align-items: center; justify-content: center; font-size: 8px; color: white; position: relative; border: 1px solid #333; }}
            .btl {{ width: 34px; height: 34px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; background-image: radial-gradient(circle at 35% 35%, rgba(255,255,255,0.2) 0%, rgba(0,0,0,0.4) 80%); }}
            .btl::after {{ content: ''; width: 10px; height: 10px; border-radius: 50%; background: rgba(0,0,0,0.7); border: 1px solid rgba(255,255,255,0.1); }}
            .btl .tooltip {{ visibility: hidden; width: 140px; background: #000; color: #fff; padding: 8px; border-radius: 4px; position: absolute; z-index: 100; bottom: 125%; left: 50%; margin-left: -70px; opacity: 0; transition: 0.3s; font-size: 10px; border-left: 3px solid #00d4ff; pointer-events: none; }}
            .btl:hover .tooltip {{ visibility: visible; opacity: 1; }}
        </style>
        </head><body>
            <button class="btn-update" onclick="window.location.reload(true);">🔄 ACTUALISER</button>
            <div class="fridge-exterior"><div class='rack'>"""

        for l in range(1, lignes + 1):
            for c in range(1, colonnes + 1):
                cid = f"{l}-{c}"
                v_plan = plan.get(cid, "")
                
                if v_plan and v_plan != "none":
                    c_recherche = slugify(v_plan)
                    couleur_brute = mapping_couleurs.get(c_recherche, "rouge")
                    
                    # Logique de couleur hexadécimale
                    h_color = "#8b0000" # Rouge
                    if "blanc" in couleur_brute: h_color = "#f4e07d" # Or
                    elif "rose" in couleur_brute: h_color = "#ff85a2" # Rose
                    
                    v_clean = v_plan.replace("'", "&apos;")
                    html += f"""<div class="slot"><div class="btl" style="background-color:{h_color}"><span class="tooltip"><b>{v_clean}</b></span></div></div>"""
                else:
                    html += f"""<div class="slot">{cid}</div>"""

        html += "</div></div></body></html>"
        
        with open(PATH_HTML, 'w', encoding='utf-8') as f:
            f.write(html)
        print("Génération réussie.")

    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    generate()
    
