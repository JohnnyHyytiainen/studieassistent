# menu.py (läggs i projektroten: .../studieassistent/menu.py)
# Den här menyn är för att lägga till kort och svara på korten.
# Kort (Lägg till kort) lägger till frågor som ställs i quiz'et. Detta för att quiz'a mig själv på de anteckningar jag har skrivit i skolan
# dels för att träna s.k spaced repetition samt för att det är en kul grej.
# Quiz (Visar korten) Här visas mina frågor som jag valt att kalla kort och lagt till och helt enkelt quiz'ar mig på det jag lagt in.
# --- imports högst upp ---
# menu.py – huvudmeny för Studieassistenten (läggs i projektroten)
from src.flashcards import add_card, quiz_once
from src.plan import set_goal, mark_done, progress, get_week, list_weeks
from src.stats import totals
# ---------------- Hjälpfunktioner ----------------


def prompt_nonempty(label: str) -> str:
    while True:
        s = input(label).strip()
        if s:
            return s
        print("Fältet får inte vara tomt. Försök igen.")


def prompt_int(label: str, default: int | None = None) -> int:
    s = input(label).strip()
    if not s and default is not None:
        return default
    try:
        return int(s)
    except ValueError:
        print("Måste vara ett heltal.")
        return prompt_int(label, default)

# ---------------- Flashcards-handlers ----------------


def handle_add_card():
    print("\n--- Lägg till kort ---")
    q = prompt_nonempty("Fråga: ")
    a = prompt_nonempty("Svar: ")
    tags_raw = input("Taggar (valfritt, separera med mellanslag): ").strip()
    tags = [t for t in tags_raw.split() if t] if tags_raw else []
    card = add_card(q, a, tags=tags)
    print(f"Lagt till: {card}")


def handle_quiz():
    print("\n--- Quiz ---")
    n = prompt_int("Hur många frågor? (t.ex. 3): ", default=3)
    correct = 0
    for i in range(1, n + 1):
        print(f"\n({i}/{n})")
        if quiz_once():
            correct += 1
    print(f"\n Klart! Rätt: {correct}/{n}")

# ---------------- Studieplan-handlers ----------------


def handle_studyplan_set():
    print("\n--- Studieplan: Sätt mål ---")
    week = prompt_int("Vecka (t.ex. 35): ")
    raw = input("Mål (kommaseparerade): ").strip()
    items = [x.strip() for x in raw.split(",") if x.strip()]
    if not items:
        print("Inga mål angivna.")
        return
    data = set_goal(week, items)
    print(f"Vecka {week} sparad:", data)


def handle_studyplan_mark():
    print("\n--- Studieplan: Markera klar ---")
    week = prompt_int("Vecka: ")
    wk = get_week(week)
    if not wk:
        print("Vecka finns inte. Sätt mål först.")
        return
    for i, item in enumerate(wk["items"]):
        status = "✔" if wk["done"][i] else "·"
        print(f"{i}: [{status}] {item}")
    idx = prompt_int("Vilket index ska markeras? (0-baserat): ")
    val = input("Klarmarkera? (j/n, default j): ").strip().lower()
    value = (val != "n")
    data = mark_done(week, idx, value)
    print("Uppdaterat:", data)


def handle_studyplan_progress():
    print("\n--- Studieplan: Progress ---")
    weeks = list_weeks()
    if not weeks:
        print("Inga veckor finns.")
        return
    print("Tillgängliga veckor:", ", ".join(weeks))
    week = prompt_int("Vecka att visa: ")
    pct = progress(week)
    wk = get_week(week)
    if not wk:
        print("Veckan saknas.")
        return
    print(f"Vecka {week}: {pct}% klart")
    for i, item in enumerate(wk["items"]):
        status = "✔" if wk["done"][i] else "·"
        print(f"  {i}: [{status}] {item}")


def handle_studyplan_menu():
    while True:
        print("\n====== STUDIEPLAN ======")
        print("1) Sätt mål för vecka")
        print("2) Markera punkt som klar")
        print("3) Visa progress")
        print("4) Tillbaka")
        choice = input("Val: ").strip()
        if choice == "1":
            handle_studyplan_set()
        elif choice == "2":
            handle_studyplan_mark()
        elif choice == "3":
            handle_studyplan_progress()
        elif choice == "4":
            break
        else:
            print("Ogiltigt val.")

# ---------------- Stats-handlers ----------------


def handle_stats():
    print("\n--- Statistik ---")
    t = totals()
    print(f"Totalt: {t['total']}")
    print(f"Rätt:   {t['correct']}")
    print(f"Fel:    {t['incorrect']}")
    print(f"Träffsäkerhet:  {t['accuracy']}%")

# ---------------- Huvudmeny ----------------


def main():
    while True:
        print("\n====== FLASHCARDS ======")
        print("1) Lägg till kort")
        print("2) Quiz")
        print("3) Studieplan")
        print("4) Statistik")
        print("5) Avsluta")
        choice = input("Val: ").strip()

        if choice == "1":
            handle_add_card()
        elif choice == "2":
            handle_quiz()
        elif choice == "5":
            print("Hejdå!")
            break
        elif choice == "3":
            handle_studyplan_menu()
        elif choice == "4":
            handle_stats()
        else:
            print("Ogiltigt val. Skriv 1, 2, 3, 4 eller 5.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAvslutar.")
