"""h7_margins_exact: точные поля обычного абзаца (ГОСТ Р 7.0.32-2017 /
7.32-2017): левое поле 30мм, правое 15мм, верхнее 20мм на A4 (210×297мм).

Жёстко: измеряем КООРДИНАТЫ, не «текст есть».
  - левый край строк-ПРОДОЛЖЕНИЙ (без абзацного отступа) x0 ≈ 85.04pt (±1);
  - правый край justify-строк (прижатых к правой границе) ≈ 552.76pt (±1);
  - верх первого слова страницы yMin ≈ 56.25pt (±1) — верхнее поле 20мм.
Левое 30мм = 85.04pt, правое поле = 595.276-552.76 = 42.52pt = 15мм.
"""
import helpers as h

c = h.Checks("h7_margins_exact")
pdf = h.compile("h7_margins_exact.typ")

ws = [w for w in h.words(pdf) if w[0] == 1 and not (w[5].isdigit() and w[2] > 700)]

# Группируем по строкам (равный yMin с допуском 0.5pt).
rows = {}
for w in ws:
    key = round(w[2] * 2) / 2
    rows.setdefault(key, []).append(w)
ordered = [rows[k] for k in sorted(rows)]

# Первая строка имеет абзацный отступ; строки-продолжения начинаются от поля.
# Берём минимальный x0 среди строк 2..N — это и есть левая граница поля.
cont_rows = ordered[1:] if len(ordered) > 1 else ordered
min_x0_cont = min(w[1] for row in cont_rows for w in row)
c.check("left_margin_continuation_85",
        abs(min_x0_cont - 85.04) < 1.0,
        f"левый край строк-продолжений x0={min_x0_cont:.3f}, ждём 85.04±1 (30мм)")

# Правый край: justify растягивает все строки кроме последней до правой границы.
# Берём максимум xMax по всем словам — должен лечь ровно на 552.76.
max_x1 = max(w[3] for w in ws)
c.check("right_margin_552",
        abs(max_x1 - 552.76) < 1.0,
        f"правый край xMax={max_x1:.3f}, ждём 552.76±1 (правое поле 15мм)")

# Верхнее поле: самое верхнее слово страницы.
top = min(ws, key=lambda t: t[2])
c.check("top_margin_56",
        abs(top[2] - 56.25) < 1.0,
        f"верх первого слова yMin={top[2]:.3f} ({top[5]!r}), ждём 56.25±1 (20мм)")

# Абзацный отступ реально есть: первая строка начинается правее границы поля.
first_x0 = min(w[1] for w in ordered[0])
c.check("paragraph_indent_present",
        first_x0 > min_x0_cont + 20,
        f"нет абзацного отступа: первая строка x0={first_x0:.2f}, "
        f"поле={min_x0_cont:.2f} (ждём отступ ~35pt = 1.25см)")

c.done()
