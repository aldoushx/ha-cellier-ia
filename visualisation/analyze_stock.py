import json
import urllib.request
import os

# --- CONFIGURATION ---
TOKEN = "VOTRE_TOKEN_ICI"
URL_INV = "http://127.0.0.1:8123/api/states/sensor.cave_a_vin_supersensor"
PATH_PLAN = "/config/cave_plan.json"

def analyze():
    try:
        # 1. RÉCUPÉRATION DE L'INVENTAIRE (SUPERSENSOR)
        req = urllib.request.Request(URL_INV)
        req.add_header('Authorization', f'Bearer {TOKEN}')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            vins_inv = data.get('attributes', {}).get('vins', {})

        stock_theorique = {}
        for entry_id, v in vins_inv.items():
            # Récupération du nom et de l'année (Clé unique)
            nom = v.get('nom', {}).get('valeur', 'Inconnu')
            annee = v.get('annee', {}).get('valeur', '')
            cle_vin = f"{nom} {annee}".strip()
            
            # Récupération directe de l'entier (selon votre structure)
            qty = int(v.get('nombre_bouteilles', 0))
            
            if cle_vin:
                stock_theorique[cle_vin] = stock_theorique.get(cle_vin, 0) + qty

        # 2. RÉCUPÉRATION DU PLAN RÉEL (JSON)
        if not os.path.exists(PATH_PLAN):
            plan = {}
        else:
            with open(PATH_PLAN, 'r', encoding='utf-8') as f:
                try:
                    plan = json.load(f)
                except:
                    plan = {}
        
        stock_reel = {}
        for vin_nom in plan.values():
            v_nom = str(vin_nom).strip()
            if v_nom != "none":
                stock_reel[v_nom] = stock_reel.get(v_nom, 0) + 1

        # 3. COMPARAISON
        erreurs = []
        # Fusion des noms de vins des deux sources pour comparaison
        tous_les_vins = sorted(list(set(list(stock_theorique.keys()) + list(stock_reel.keys()))))
        
        for vin in tous_les_vins:
            theo = stock_theorique.get(vin, 0)
            reel = stock_reel.get(vin, 0)
            
            if reel < theo:
                erreurs.append(f"⚠️ **{vin}** : {theo-reel} manquante(s) sur le plan")
            elif reel > theo:
                erreurs.append(f"🚫 **{vin}** : {reel-theo} en trop (non inventoriée)")

        return {
            "total_inv": sum(stock_theorique.values()),
            "total_plan": sum(stock_reel.values()),
            "details": erreurs if erreurs else ["✅ Toutes les bouteilles sont rangées !"]
        }
    except Exception as e:
        return {"total_inv": 0, "total_plan": 0, "details": [f"Erreur technique: {str(e)}"]}

if __name__ == "__main__":
    print(json.dumps(analyze()))
    
