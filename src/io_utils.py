import json
from pathlib import Path


def write_json(path, data):
    """
    Spara ett Python-objekt (t.ex. lista eller dict) till en JSON-fil.
    - path: sökvägen till filen, t.ex. 'data/test.json'
    - data: objektet som ska sparas
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)  # säkerställ att mappen finns
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_json(path, default=None):
    """
    Läs en JSON-fil.
    - path: sökvägen till filen
    - default: vad som returneras om filen inte finns
    """
    p = Path(path)
    if not p.exists():
        return default
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)
