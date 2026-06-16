"""he3_long_table_continuation_count: очень длинная таблица (80 строк) на
3+ страницы. Строгие инварианты переноса:

1. Число «Продолжение» == число ДОПОЛНИТЕЛЬНЫХ страниц (всего страниц − 1).
2. На КАЖДОЙ продолжающей странице первое слово — «Продолжение», и оно
   стоит у верхнего поля (yMin ≈ 56.25, не съезжает вниз).
3. Номер таблицы стабилен: каждая «Продолжение таблицы N» содержит N == 1
   (таблица одна), нумерация не плывёт.
4. Ни одна строка данных не потеряна и не продублирована при разрыве."""
import re
import helpers as h

c = h.Checks("he3_long_table_continuation_count")
pdf = h.compile("he3_long_table_continuation_count.typ")
ws = h.words(pdf)
n = h.page_count(pdf)

c.check("spans_3plus_pages", n >= 3, f"таблица заняла лишь {n} страниц, нужно 3+")

cont_words = [w for w in ws if w[5] == "Продолжение"]
c.check("cont_eq_extra_pages",
        len(cont_words) == n - 1,
        f"'Продолжение' {len(cont_words)} раз, доп.страниц {n - 1}")

# Каждая продолжающая страница (2..n): первое слово — «Продолжение», у верха.
bad_first = []
for p in range(2, n + 1):
    fw = h.first_word(pdf, p)
    if fw is None or fw[1] != "Продолжение" or fw[0] > 60:
        bad_first.append((p, fw))
c.check("cont_at_top_each_page",
        not bad_first,
        f"продолжение не у верхнего поля / не первое слово: {bad_first}")

# Номер таблицы стабилен == 1 во всех «Продолжение таблицы N».
t = " ".join(h.text(pdf).split())
nums = re.findall(r"Продолжение таблицы\s*([0-9]+)", t)
c.check("table_number_stable",
        nums and all(x == "1" for x in nums),
        f"номер таблицы в продолжениях не стабилен (== '1'): {nums}")

# Все 80 строк присутствуют ровно один раз (нет потерь/дублей при разрыве).
keys = [w[5] for w in ws if re.match(r"^К[0-9]+$", w[5])]
import collections
cnt = collections.Counter(keys)
dups = [k for k, v in cnt.items() if v > 1]
missing = [f"К{i}" for i in range(1, 81) if f"К{i}" not in cnt]
c.check("no_lost_or_dup_rows",
        not dups and not missing,
        f"дубли={dups[:5]} пропуски={missing[:5]}")

c.done()
