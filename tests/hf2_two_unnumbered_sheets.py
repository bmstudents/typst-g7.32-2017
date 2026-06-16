"""hf2: БАГ усиливается — ДВА листа вне нумерации в начале дают три «1».

Файл пакета: gost732-2017/utils/insert.typ:48-50 (clamp calc.max(n-1,1)).

Типичный диплом начинается с титула и задания, оба печатаются вне сквозной
нумерации (`в-нумерации: false`). Из-за floor `calc.max(n-1,1)` счётчик на
старте «залипает» на 1: каждый ведущий лист вне нумерации снова обнуляет
декремент до 1, поэтому первые ТРИ страницы получают «1».

Фактические футеры (текстовый слой):
    стр.1 (титул)   = «1»
    стр.2 (задание) = «1»
    стр.3 (реферат) = «1»   ← все три одинаковые
    стр.4 (содерж.) = «2»
    стр.5 (введ.)   = «3»

Инвариант: номера страниц во всём документе строго уникальны и монотонно
возрастают. Тройной «1» обязан валить тест.
"""
import helpers as h

c = h.Checks("hf2_two_unnumbered_sheets")
pdf = h.compile("hf2_two_unnumbered_sheets.typ")

n = h.page_count(pdf)
c.check("five_pages", n == 5, f"страниц {n}, ждём 5")

footers = []
for p in range(1, n + 1):
    nums = [w for w in h.words(pdf) if w[0] == p and w[2] > 700 and w[5].isdigit()]
    footers.append(nums[0][5] if nums else None)

non_none = [f for f in footers if f is not None]

# ИНВАРИАНТ 1: уникальность номеров (никаких трёх «1»).
c.check("all_page_numbers_unique",
        len(non_none) == len(set(non_none)),
        f"номера страниц повторяются: {footers} "
        f"(insert.typ:49 floor calc.max(n-1,1) — ведущие листы вне нумерации "
        f"залипают на '1')")

# ИНВАРИАНТ 2: значение «1» встречается не более одного раза.
c.check("only_one_page_one",
        non_none.count("1") <= 1,
        f"номер '1' встречается {non_none.count('1')} раз(а): {footers}")

# ИНВАРИАНТ 3: вся последовательность номеров строго возрастает.
strictly_inc = all(
    non_none[i] is not None and int(non_none[i + 1]) > int(non_none[i])
    for i in range(len(non_none) - 1)
)
c.check("strictly_increasing",
        strictly_inc,
        f"номера страниц не строго возрастают: {footers}")

c.done()
