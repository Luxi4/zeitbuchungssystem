import json
import uuid
from pathlib import Path

PFAD = Path("user_data.json")

def lade_nutzer():
    if not PFAD.exists():
        return []
    with open(PFAD, "r", encoding="utf-8") as f:
        return json.load(f)

def speichere_nutzer(neuer_nutzer):
    daten = lade_nutzer()
    daten.append(neuer_nutzer)
    with open(PFAD, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=2)

def aktiviere_nutzer(bestätigungscode):
    daten = lade_nutzer()
    for nutzer in daten:
        if nutzer["code"] == bestätigungscode:
            nutzer["ist_aktiv"] = True
            break
    with open(PFAD, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=2)