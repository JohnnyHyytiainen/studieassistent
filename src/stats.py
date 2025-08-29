# src/stats.py
"""
stats.py – beräkning av övergripande quiz-statistik.

Läser data/results.csv (skapad av flashcards.quiz_once) och räknar:
- total antal frågor
- antal rätt
- antal fel
- träffsäkerhet i procent (avrundat till heltal)
"""

from pathlib import Path
from typing import List, Dict, Any
import csv

RESULTS_CSV = Path("data/results.csv")


def load_results() -> list[dict[str, Any]]:
    """
    Läs in results.csv och returnera rader som dicts.

    CSV-format:
        timestamp,question,expected,given,correct

    Returns:
        list[dict[str, Any]]: en lista med rader; tom lista om filen saknas.
    """

    if not RESULTS_CSV.exists():
        return []

    rows: List[Dict[str, Any]] = []
    with RESULTS_CSV.open("r", newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        first = next(r, None)

        # Kolla om första raden är header
        header = ["timestamp", "question", "expected", "given", "correct"]
        if first and [c.strip().lower() for c in first] != header:
            # Första raden är data, inte header → behandla den som data
            if len(first) >= 5:
                rows.append({
                    "timestamp": first[0],
                    "question": first[1],
                    "expected": first[2],
                    "given": first[3],
                    "correct": first[4],
                })

        for row in r:
            if len(row) < 5:
                continue
            rows.append({
                "timestamp": row[0],
                "question": row[1],
                "expected": row[2],
                "given": row[3],
                "correct": row[4],
            })
    return rows


def totals() -> dict[str, int]:
    """
    Summera quiz-resultat.

    Returns:
        dict[str, int]: {
            "total": antal frågor,
            "correct": antal rätt,
            "incorrect": antal fel,
            "accuracy": procent (0–100)
        }
    """

    data = load_results()
    total = len(data)
    correct = sum(1 for d in data if str(
        d["correct"]).strip() in ("1", "true", "True"))
    incorrect = total - correct
    accuracy = int(round(100 * correct / total)) if total else 0
    return {"total": total, "correct": correct, "incorrect": incorrect, "accuracy": accuracy}
