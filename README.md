# Studieassistenten (Flashcards + Studieplan + Statistik)

Ett terminalbaserat verktyg för egen studieträning:
- **Flashcards**: skapa frågor och svar för att quiza dig själv.
- **Studieplan**: sätt veckomål, bocka av, se progress i %.
- **Statistik**: totals, rätt och fel, total rätt/fel i %.
- **Generator**: skapa kort automatiskt från `data/concepts.json`.

----------

## Snabbstart
```bash
python menu.py

----------

Meny

1: Lägga till kort – skriv fråga/svar (valfritt taggar).

2: Quiz – svara på slumpade kort (loggas till data/results.csv).

3: Studieplan – sätt mål för en vecka, markera klart, visa % klart.

4: Statistik – total, rätt, fel, totala rätt/fel i %.

5: Generera flashcards – läs data/concepts.json och skapa kort.

6: Avsluta

----------

Projektstruktur

studieassistent/
├─ menu.py                  # huvudmeny
├─ src/
│  ├─ io_utils.py           # läs/skriv JSON
│  ├─ flashcards.py         # add_card, quiz_once (loggar till CSV)
│  ├─ plan.py               # set_goal, mark_done, progress
│  ├─ stats.py              # totals() från results.csv
│  └─ generator.py          # generate_questions() från concepts.json
├─ data/
│  ├─ flashcards.json       # alla kort (Q/A)
│  ├─ results.csv           # quiz-logg
│  ├─ plan.json             # veckomål
│  └─ concepts.json         # begrepp för generatorn
└─ tests/
   ├─ manual_flashcards.py  # seed/quiz (manuellt)
   ├─ plan_manual.py        # test för plan
   └─ stats_manual.py       # test för statistik

----------

Datafiler

* data/flashcards.json – lista av kort

[{"q": "Vad är int i Python?", "a": "heltal", "tags": ["python","bas"]}]

* data/results.csv – logg av quiz-resultat

timestamp,question,expected,given,correct
2025-08-23T20:47:56,Vad gör len('abc') i Python?,3,Lenght 3,0

* data/plan.json – veckomål

{"35": { "items": ["Lägg till 5 kort"], "done": [true] }}

* data/concepts.json – begrepp att generera frågor från

[{"term": "int", "lang": "python", "def": "heltal", "hint": "42"}]

----------

FAQ

Q: ModuleNotFoundError: No module named 'src.something'
A: Kör kommandon från projektroten (mappen där menu.py ligger).

Q: “Inga resultat ännu” i Statistik
A: Kör ett quiz först – results.csv skapas vid första försöket.

Q: Jag får dubletter av kort
A: Kör tests/dedupe_cards.py eller rensa manuellt.

----------

Roadmap (efter v1.0)

1: Filtera quiz per tag (t.ex. bara python).

2: Snällare rättning (synonymer, stavfel).

3: Export av statistik (per dag/vecka).

4: Visualiseringar eller GUI-version.

----------