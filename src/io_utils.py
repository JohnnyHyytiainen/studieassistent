"""
io_utils.py – hjälpfunktioner för att läsa och skriva JSON-filer.

Denna modul används i hela projektet för att hantera datafiler
på ett konsekvent sätt. Den ser till att mappar finns och att
JSON-data sparas/lästs på ett säkert sätt.
"""
import json
from pathlib import Path


def write_json(path, data):
    """
    Spara ett Python-objekt (lista eller dict) till en JSON-fil.

    Args:
        path (str | Path): sökväg till filen, ex. 'data/test.json'
        data (any): objektet som ska sparas

    Returns:
        None
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)  # säkerställ att mappen finns
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_json(path, default=None):
    """
    Läs en JSON-fil från given sökväg.

    Args:
        path (str | Path): sökväg till filen
        default (any, optional): returvärde om filen inte finns. Standard: None

    Returns:
        Objektet som fanns i JSON-filen, eller `default` om filen saknas.
    """
    p = Path(path)
    if not p.exists():
        return default
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)
