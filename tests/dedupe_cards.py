# tests/dedupe_cards.py
# Skript för att rensa dupes av kort. Alltså kopior.
from pathlib import Path
from src.io_utils import read_json, write_json

CARDS_PATH = Path("data/flashcards.json")
BACKUP = Path("data/flashcards.backup.json")


def norm(s: str) -> str:
    return " ".join((s or "").strip().lower().split())


def main():
    cards = read_json(CARDS_PATH, default=[])
    if not isinstance(cards, list):
        raise SystemExit("flashcards.json måste vara en lista")
    # Backup
    write_json(BACKUP, cards)

    seen = set()
    unique = []
    for c in cards:
        q = c.get("q", "")
        a = c.get("a", "")
        key = (norm(q), norm(a))
        if key in seen:
            continue
        seen.add(key)
        # normalisera tags lite
        tags = c.get("tags", [])
        tags = sorted({t.strip() for t in tags if t and t.strip()})
        unique.append({"q": q, "a": a, "tags": tags})

    write_json(CARDS_PATH, unique)
    print(f" Klart. {len(cards)} → {len(unique)} kort. Backup: {BACKUP}")


if __name__ == "__main__":
    main()
