# src/plan.py
from pathlib import Path
from typing import List, Dict, Any
from src.io_utils import read_json, write_json

PLAN_PATH = Path("data/plan.json")


# ---------------- Hjälpare ----------------
def _load_plan() -> Dict[str, Dict[str, Any]]:
    data = read_json(PLAN_PATH, default={})
    if not isinstance(data, dict):
        raise ValueError(
            "plan.json måste vara ett dict {vecka: {items: [...], done: [...]}}.")
    return data


def _save_plan(plan: Dict[str, Dict[str, Any]]) -> None:
    write_json(PLAN_PATH, plan)


def _norm_week(week: int | str) -> str:
    """
    Normalisera vecka till str. Tillåter 35 eller "35".
    """
    return str(week).strip()


# ---------------- Publika funktioner ----------------
def set_goal(week: int, items: List[str]) -> Dict[str, Any]:
    """
    Sätt veckomål för given vecka.
    Exempel:
      set_goal(35, ["Lägg till 5 kort", "Kör 10 quiz-frågor", "Läs 45 min kurs"])
    Lagring i data/plan.json:
      {
        "35": {
          "items": [...],
          "done":  [False, ...]
        }
      }
    """
    w = _norm_week(week)
    clean = [s.strip() for s in (items or []) if s and s.strip()]
    if not clean:
        raise ValueError("items måste innehålla minst en icke-tom sträng.")

    plan = _load_plan()
    plan[w] = {
        "items": clean,
        "done": [False] * len(clean),
    }
    _save_plan(plan)
    return plan[w]


def mark_done(week: int, item_index: int, value: bool = True) -> Dict[str, Any]:
    """
    Markera ett mål som klart/inte klart.
    item_index är 0-baserat (första punkten = 0).
    """
    w = _norm_week(week)
    plan = _load_plan()
    if w not in plan:
        raise KeyError(f"Vecka {w} saknas. Sätt mål först med set_goal().")

    items = plan[w].get("items", [])
    done = plan[w].get("done", [False] * len(items))

    if not (0 <= item_index < len(items)):
        raise IndexError(
            f"item_index {item_index} ligger utanför intervallet 0..{len(items)-1}.")

    done[item_index] = bool(value)
    plan[w]["done"] = done
    _save_plan(plan)
    return plan[w]


def progress(week: int) -> int:
    """
    Returnerar progress i % för veckan (avrundad till heltal).
    Tom vecka eller inga items => 0%.
    """
    w = _norm_week(week)
    plan = _load_plan()
    if w not in plan:
        return 0

    items = plan[w].get("items", [])
    done = plan[w].get("done", [False] * len(items))

    if not items:
        return 0

    pct = round(100 * (sum(1 for d in done if d) / len(items)))
    return pct


# (Valfria extra-hjälpare om du vill använda senare i menyn)
def get_week(week: int) -> Dict[str, Any] | None:
    w = _norm_week(week)
    plan = _load_plan()
    return plan.get(w)


def list_weeks() -> List[str]:
    plan = _load_plan()
    return sorted(plan.keys(), key=lambda x: int(x) if x.isdigit() else x)
