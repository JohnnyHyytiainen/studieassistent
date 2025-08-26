# src/stats.py
from pathlib import Path
from typing import List, Dict, Any
import csv

RESULTS_CSV = Path("data/results.csv")


def load_results() -> List[Dict[str, Any]]:
    """
    Läser results.csv och returnerar en lista av rader som dicts:
    {"timestamp": ..., "question": ..., "expected": ..., "given": ..., "correct": "1"/"0"}
    Tom lista om filen saknas.
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


def totals() -> Dict[str, int]:
    """
    Returnerar en sammanfattning:
      {"total": N, "correct": C, "incorrect": N-C, "accuracy": procent_heltal}
    """
    data = load_results()
    total = len(data)
    correct = sum(1 for d in data if str(
        d["correct"]).strip() in ("1", "true", "True"))
    incorrect = total - correct
    accuracy = int(round(100 * correct / total)) if total else 0
    return {"total": total, "correct": correct, "incorrect": incorrect, "accuracy": accuracy}
