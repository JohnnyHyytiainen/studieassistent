# tests/manual_flashcards.py
from src.flashcards import add_card, quiz_once


def seed():  # Varför seed scrips? Jag kan återvända och fylla på med fler kort snabbt.
    add_card("Vad gör len('abc') i Python?", "3", tags=["python", "bas"])
    add_card("SQL: vad gör GROUP BY?",
             "Grupperar rader för aggregat", tags=["sql"])
    add_card("Vad betyder idempotent i datajobb?",
             "Upprepad körning ändrar inte resultatet", tags=["etl"])


if __name__ == "__main__":
    # 1) Lägg in tre kort
    seed()
    print("Lagt till 3 kort i data/flashcards.json")

    # 2) Kör quiz tre gånger
    print("\nKör quiz tre gånger:")
    for _ in range(3):
        quiz_once()
