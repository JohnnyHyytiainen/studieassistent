# tests/manual_generate.py
from pathlib import Path
from src.generator import generate_questions, CONCEPTS_PATH

print("Genererar frågor från:", CONCEPTS_PATH)
added = generate_questions(CONCEPTS_PATH, per_term=1)
print(f"Klart. Lades till {added} nya kort.")
