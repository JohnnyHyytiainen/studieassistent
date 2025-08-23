from src.flashcards import add_card  # Lägger manuellt till kort.

added = add_card(
    "Vad kallas ett heltal, en text och ett tal med decimaler i python?",
    "3",
    tags=["python", "bas"]
)
print("Lagt till:", added)
