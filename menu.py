# menu.py (läggs i projektroten: .../studieassistent/menu.py)
# Den här menyn är för att lägga till kort och svara på korten.
# Kort (Lägg till kort) lägger till frågor som ställs i quiz'et. Detta för att quiz'a mig själv på de anteckningar jag har skrivit i skolan
# dels för att träna s.k spaced repetition samt för att det är en kul grej.
# Quiz (Visar korten) Här visas mina frågor som jag valt att kalla kort och lagt till och helt enkelt quiz'ar mig på det jag lagt in.
from src.flashcards import add_card, quiz_once


def prompt_nonempty(label: str) -> str:
    while True:
        s = input(label).strip()
        if s:
            return s
        print("Fältet får inte vara tomt. Försök igen.")


def handle_add_card():
    print("\n--- Lägg till kort ---")
    q = prompt_nonempty("Fråga: ")
    a = prompt_nonempty("Svar: ")
    tags_raw = input("Taggar (valfritt, separera med mellanslag): ").strip()
    tags = [t for t in tags_raw.split() if t] if tags_raw else []
    card = add_card(q, a, tags=tags)
    print(f" Lagt till: {card}")


def handle_quiz():
    print("\n--- Quiz ---")
    try:
        n = int(input("Hur många frågor? (t.ex. 3): ").strip() or "3")
    except ValueError:
        n = 3
    correct = 0
    for i in range(1, n + 1):
        print(f"\n({i}/{n})")
        if quiz_once():
            correct += 1
    print(f"\n Klart! Rätt: {correct}/{n}")


def main():
    while True:
        print("\n====== FLASHCARDS ======")
        print("1) Lägg till kort")
        print("2) Quiz")
        print("3) Avsluta")
        choice = input("Val: ").strip()

        if choice == "1":
            handle_add_card()
        elif choice == "2":
            handle_quiz()
        elif choice == "3":
            print("Hejdå!")
            break
        else:
            print("Ogiltigt val. Skriv 1, 2 eller 3.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAvslutar.")
