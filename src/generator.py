# src/generator.py
from pathlib import Path
from typing import List, Dict, Any
from src.io_utils import read_json
from src.flashcards import add_card, FLASHCARDS_PATH

CONCEPTS_PATH = Path("data/concepts.json")


def _norm(s: str) -> str:
    return " ".join((s or "").strip().lower().split())


def _card_exists(q: str, a: str) -> bool:
    """
    Kolla om ett kort med samma (q, a) redan finns — case/whitespace-okänsligt.
    """
    cards = read_json(FLASHCARDS_PATH, default=[])
    if not isinstance(cards, list):
        return False
    nq, na = _norm(q), _norm(a)
    for c in cards:
        if _norm(c.get("q", "")) == nq and _norm(c.get("a", "")) == na:
            return True
    return False


def _build_question(term: str, lang: str) -> str:
    lang = (lang or "").strip().lower()
    term = (term or "").strip()
    if lang == "python" and term:
        return f"Vad är {term} i Python?"
    if term:
        return f"Vad är {term}?"
    return ""


def generate_questions(concepts_path: Path = CONCEPTS_PATH, per_term: int = 1) -> int:
    """
    Läser data/concepts.json och lägger till enkla Q/A i flashcards.
    - per_term: hur många frågor per begrepp (1 räcker fint för vår strikta rättning).
    Returnerar antal NYA kort som lades till.
    """
    data = read_json(concepts_path, default=[])
    if not isinstance(data, list):
        raise ValueError("concepts.json måste vara en lista av objekt.")

    added = 0
    for item in data:
        term = (item.get("term") or "").strip()
        lang = (item.get("lang") or "").strip()
        definition = (item.get("def") or "").strip()
        hint = (item.get("hint") or "").strip()

        if not term or not definition:
            continue

        # Fråga 1: "Vad är <term> i Python?"
        q1 = _build_question(term, lang)
        a1 = definition  # håll kort för exakt rättning
        if q1 and not _card_exists(q1, a1):
            add_card(q1, a1, tags=[lang or "okänd", "auto"])
            added += 1

        # Valfri extra-variant (per_term > 1): en neutral formulering
        if per_term > 1:
            q2 = f"Beskriv {term} kort"
            a2 = definition
            if not _card_exists(q2, a2):
                add_card(q2, a2, tags=[lang or "okänd", "auto"])
                added += 1

    return added
