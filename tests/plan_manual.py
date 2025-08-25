# tests/plan_manual.py
from src.plan import set_goal, mark_done, progress, get_week

# 1) Sätt mål för vecka 35
week = 35
goals = ["Lägg till 5 kort", "Kör 10 quiz-frågor", "Läs 45 min kurs"]
print("Sätter mål vecka 35:", goals)
print(set_goal(week, goals))

# 2) Kolla progress = 0%
print("Progress (0% väntat):", progress(week), "%")

# 3) Markera första punkten som klar (index 0)
print("Markerar punkt 0 klar")
print(mark_done(week, 0, True))
print("Progress (~33% väntat):", progress(week), "%")

# 4) Markera andra punkten som klar
print("Markerar punkt 1 klar")
print(mark_done(week, 1, True))
print("Progress (~67% väntat):", progress(week), "%")

# 5) Markera tredje punkten som klar
print("Markerar punkt 2 klar")
print(mark_done(week, 2, True))
print("Progress (100% väntat):", progress(week), "%")

# 6) Läs tillbaka veckan
print("Hämtar vecka 35:", get_week(35))
