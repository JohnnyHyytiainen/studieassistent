"""
plan.py – hantering av studieplan med veckomål.

Denna modul lagrar mål i data/plan.json.
Den kan:
- sätta nya mål för en vecka (set_goal)
- markera en punkt som klar (mark_done)
- beräkna progress i procent (progress)

Dataformat (plan.json):
{
    "35": { "items": ["Läs kapitel 1", "Träna loops"], "done": [true, false] },
    "36": { ... }
}
"""

from pathlib import Path
from typing import Any
from src.io_utils import read_json, write_json

PLAN_PATH = Path("data/plan.json")


# ---------------- Hjälpare ----------------
def _load_plan() -> dict[str, dict[str, Any]]:
    """
    Läs in hela planen från data/plan.json.

    Returns:
        dict[str, dict]: {"vecka": {"items": [...], "done": [...]}}

    Raises:
        ValueError: om filformatet inte är ett dict
    """
    data = read_json(PLAN_PATH, default={})
    if not isinstance(data, dict):
        raise ValueError(
            "plan.json måste vara ett dict {vecka: {items: [...], done: [...]}}."
        )
    return data


def _save_plan(plan: dict[str, dict[str, Any]]) -> None:
    """
    Spara hela planen till data/plan.json.

    Args:
        plan (dict): planen som ska sparas
    """
    write_json(PLAN_PATH, plan)


def _norm_week(week: int | str) -> str:
    """
    Normalisera vecka till str. Tillåter 35 eller "35".
    """
    return str(week).strip()


# ---------------- Publika funktioner ----------------
def set_goal(week: int, items: list[str]) -> dict[str, Any]:
    """
    Sätt mål för en vecka.

    Args:
        week (int): veckonummer, ex. 35
        items (list[str]): lista med målbeskrivningar

    Returns:
        dict[str, Any]: den uppdaterade veckans data (items + done-lista)
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


def mark_done(week: int, item_index: int, value: bool = True) -> dict[str, Any]:
    """
    Markera en specifik punkt som klar/ej klar.

    Args:
        week (int): veckonummer
        item_index (int): index i listan items (0-baserat)
        value (bool, optional): True = klar, False = ej klar. Standard: True.

    Returns:
        dict[str, Any]: den uppdaterade veckans data
    """
    w = _norm_week(week)
    plan = _load_plan()
    if w not in plan:
        raise KeyError(f"Vecka {w} saknas. Sätt mål först med set_goal().")

    items = plan[w].get("items", [])
    done = plan[w].get("done", [False] * len(items))

    if not (0 <= item_index < len(items)):
        raise IndexError(
            f"item_index {item_index} ligger utanför intervallet 0..{len(items)-1}."
        )

    done[item_index] = bool(value)
    plan[w]["done"] = done
    _save_plan(plan)
    return plan[w]


def progress(week: int) -> int:
    """
    Beräkna hur många procent av målen som är klara för given vecka.

    Args:
        week (int): veckonummer

    Returns:
        int: procent (0–100). Returnerar 0 om inga mål finns.
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


def get_week(week: int) -> dict[str, Any] | None:
    """
    Hämta data för en vecka.

    Args:
        week (int): veckonummer

    Returns:
        dict[str, Any] | None: veckans data, eller None om den saknas
    """
    w = _norm_week(week)
    plan = _load_plan()
    return plan.get(w)


def list_weeks() -> list[str]:
    """
    Lista alla veckonummer som finns sparade i plan.json.

    Returns:
        list[str]: veckonummer som strängar (sorterade numeriskt när möjligt)
    """
    plan = _load_plan()
    return sorted(plan.keys(), key=lambda x: int(x) if x.isdigit() else x)
