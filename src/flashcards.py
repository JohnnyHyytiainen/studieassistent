"""
flashcards.py – hantering av frågekort (Q/A) och quiz.

Denna modul lagrar kort i data/flashcards.json, kan lägga till nya kort,
och köra quiz där frågor slumpas fram. Svar loggas i data/results.csv
för att möjliggöra statistik.
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime
import random
import csv
from typing import List, Dict, Optional
from src.io_utils import read_json, write_json

# Filvägar
FLASHCARDS_PATH = Path("data/flashcards.json")
RESULTS_CSV = Path("data/results.csv")

# ----- Hjälpare för att läsa/spara kort -----


def _load_cards() -> List[Dict]:
    """
    Läs in alla flashcards från data/flashcards.json.

    Returns:
        list[dict]: en lista med kort-objekt ({"q": fråga, "a": svar, "tags": []})

    Raises:
        ValueError: om filen inte innehåller en lista
    """
    cards = read_json(FLASHCARDS_PATH, default=[])
    if not isinstance(cards, list):
        raise ValueError("flashcards.json måste vara en lista av kort.")
    return cards


def _save_cards(cards: List[Dict]) -> None:
    """
    Spara hela listan av kort till data/flashcards.json.

    Args:
        cards (list[dict]): korten som ska sparas

    Returns:
        None
    """
    write_json(FLASHCARDS_PATH, cards)

# ----- Publik funktion: lägg till kort -----


def add_card(question: str, answer: str, tags: Optional[List[str]] = None) -> Dict:
    """
    Lägg till ett nytt kort.

    Args:
        question (str): frågetext
        answer (str): korrekt svar
        tags (list[str], optional): kategorier (t.ex. ["python","bas"])

    Returns:
        dict: kortet som lades till
    """
    q = (question or "").strip()
    a = (answer or "").strip()
    if not q or not a:
        raise ValueError("Både fråga och svar måste ha innehåll.")
    card = {"q": q, "a": a, "tags": tags or []}
    cards = _load_cards()
    cards.append(card)
    _save_cards(cards)
    return card

# ----- Hjälpare för quiz -----


def _normalize(s: str) -> str:
    # Trimma, gör till lowercase och komprimera mellanslag
    return " ".join((s or "").strip().lower().split())


def _ensure_results_header():
    # Skapa mapp/fil och skriv header om results.csv inte finns
    RESULTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    if not RESULTS_CSV.exists():
        with RESULTS_CSV.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["timestamp", "question",
                       "expected", "given", "correct"])

# ----- Publik funktion: kör ett quiz -----


def quiz_once() -> bool:
    """
    Ställ en slumpmässig fråga, ta in användarens svar och jämför med facit.

    Returns:
        bool: True om användaren svarade rätt, False annars

    Biverkan:
        - Loggar frågan, rätt svar, användarens svar och om det var rätt/fel
          till data/results.csv
    """
    cards = _load_cards()
    if not cards:
        print("Inga kort ännu. Lägg till med add_card(...).")
        return False

    card = random.choice(cards)

    print("\nFRÅGA:")
    print(card["q"])
    given = input("\nDitt svar: ").strip()

    expected = card["a"]
    correct = _normalize(given) == _normalize(expected)

    if correct:
        print("Rätt!")
    else:
        print(f"Fel. Rätt svar: {expected}")

    _ensure_results_header()
    with RESULTS_CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            datetime.now().isoformat(timespec="seconds"),
            card["q"],
            expected,
            given,
            "1" if correct else "0",
        ])
    return correct
