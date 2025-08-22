from src.io_utils import write_json, read_json

# Vart vi vill spara vår testfil
DATA_PATH = "data/test.json"

# Vårt testdata (en enkel lista)
payload = ["alpha", "beta", "gamma"]

print("=> Skriver...")
write_json(DATA_PATH, payload)

print("=> Läser...")
result = read_json(DATA_PATH)

# Kontrollera att det vi läser är samma som vi skrev
assert result == payload, f"Förväntade {payload}, fick {result}"
print("✅ Test OK. Filen finns och innehållet matchar.")
