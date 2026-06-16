"""he4: листинги в комбинации. Три листинга вперемежку с рисунком ->
Листинг 1,2,3 (свой счётчик, не сбит рисунком). Длинный листинг 3
переносится на след. страницы с подписью «Продолжение листинга 3»
(верный номер), подпись «Листинг 3» НЕ отрывается от первой строки кода
(orphan-защита), выравнивание тела и шапки одинаково на всех страницах.
"""
import re
import helpers as h

c = h.Checks("he4_listing_combo")
pdf = h.compile("he4_listing_combo.typ")
ws = h.words(pdf)
t = " ".join(h.text(pdf).split())

# --- сквозная нумерация листингов, независимая от рисунка ---
nums = re.findall(r"Листинг (\d+)", t)
c.check("listing_sequential", nums == ["1", "2", "3"],
        f"листинги не сквозные 1,2,3 (рисунок не должен сбивать счётчик): {nums}")

# --- продолжение длинного листинга подписано тем же номером (3) ---
conts = set(re.findall(r"Продолжение листинга (\d+)", t))
c.check("continuation_present", len(conts) >= 1,
        "длинный листинг не дал ни одной 'Продолжение листинга N'")
c.check("continuation_number_correct", conts == {"3"},
        f"номер в продолжении листинга неверен: {conts}, ожидался только '3'")

# --- подпись 'Листинг 3' не оторвана: на её странице ниже есть код ---
listings = [w for w in ws if w[5] == "Листинг"]
c.check("three_captions", len(listings) == 3, f"найдено подписей Листинг: {len(listings)}")
if len(listings) == 3:
    p3, y3 = listings[2][0], listings[2][2]
    code_below = [w for w in ws if w[0] == p3 and w[2] > y3 and w[5] == "def"]
    c.check("caption3_not_orphan", len(code_below) >= 1,
            "подпись 'Листинг 3' оторвана от кода (нет строк кода ниже неё на той же странице)")

# --- выравнивание: код начинается в одной x-колонке на всех страницах ---
def_x = {}
for w in ws:
    if w[5] == "def":
        def_x.setdefault(w[0], []).append(w[1])
left_per_page = {p: round(min(xs), 1) for p, xs in def_x.items()}
distinct_left = set(left_per_page.values())
c.check("code_left_consistent", len(distinct_left) == 1,
        f"левый край кода различается по страницам: {left_per_page}")

# --- шапка 'Продолжение' на левом поле, одинаково на всех страницах ---
cont_x = [round(w[1], 1) for w in ws if w[5] == "Продолжение"]
c.check("continuation_left_consistent",
        len(set(cont_x)) == 1 and cont_x,
        f"шапка продолжения смещается по страницам: {cont_x}")

c.done()
