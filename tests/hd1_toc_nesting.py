"""hd1_toc_nesting: вложенность 1 / 1.1 / 1.1.1 / 1.1.1.1 в TOC.

- Все уровни попадают в TOC с корректным иерархическим номером.
- Отступ растёт с уровнем: x(номера) строго увеличивается L1<L2<L3<L4.
- Нормализованный текст содержит номера в правильном порядке.
"""
import helpers as h

c = h.Checks("hd1_toc_nesting")
pdf = h.compile("hd1_toc_nesting.typ")
ws = h.words(pdf)
toc_page = min((w[0] for w in ws if w[5] == "СОДЕРЖАНИЕ"), default=1)
toc_ws = [w for w in ws if w[0] == toc_page]
norm = " ".join(h.text(pdf).split())

# Ожидаемые номера в TOC и их уровень
EXPECT = [
    ("1", 1, "Первый"),
    ("1.1", 2, "Подраздел"),
    ("1.1.1", 3, "Пункт"),
    ("1.1.1.1", 4, "Подпункт"),
    ("2", 1, "Второй"),
    ("2.1", 2, "Подраздел"),
    ("2.1.1", 3, "Пункт"),
]

# x-координата номера каждого уровня (по первому вхождению номера-токена в TOC)
x_by_level = {}
for num, lvl, _ in EXPECT:
    hit = next((w for w in toc_ws if w[5] == num), None)
    c.check(f"num_{num}_present", hit is not None,
            f"номер {num!r} (уровень {lvl}) отсутствует в TOC")
    if hit is not None and lvl not in x_by_level:
        x_by_level[lvl] = hit[1]

# Отступ растёт строго с уровнем
levels = sorted(x_by_level)
inc = all(x_by_level[levels[i]] < x_by_level[levels[i + 1]] for i in range(len(levels) - 1))
c.check("indent_increases", inc,
        f"отступы по уровням не возрастают: {{l:round(x) for l,x in x_by_level.items()}} -> "
        + str({l: round(x, 1) for l, x in x_by_level.items()})
        + ". Файл: gost732-2017/styles/toc.typ (indent_amount)")

# Порядок номеров в нормализованном тексте: 1 ... 1.1 ... 1.1.1 ... 1.1.1.1 ... 2 ...
seq = ["1", "1.1", "1.1.1", "1.1.1.1", "2", "2.1", "2.1.1"]
pos = []
ok_order = True
search_from = 0
for token in seq:
    # ищем токен как отдельное «слово» в TOC-части (до начала тела)
    idx = norm.find(token + " ", search_from)
    if idx < 0:
        ok_order = False
        break
    pos.append(idx)
    search_from = idx + len(token)
c.check("number_order", ok_order and pos == sorted(pos),
        f"иерархические номера в TOC идут не по порядку: {seq} позиции {pos}")

c.done()
