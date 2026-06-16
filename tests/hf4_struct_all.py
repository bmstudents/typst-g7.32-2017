"""hf4_struct_all: текст и регистр КАЖДОЙ структурной константы (русские).

ГОСТ 7.32-2017: заголовки структурных элементов — ПРОПИСНЫМИ, по центру,
без номера. Проверяем, что в текстовом слое присутствует именно прописная
форма каждого заголовка и что ни один из них не пронумерован.

Это контрольная группа к hf4_struct_perechen: эти пять заголовков ведут
себя корректно, что доказывает — баг с «Перечень сокращений и ссылок»
именно в рассинхроне константы и регэкспа, а не в общей механике.
"""
import helpers as h

c = h.Checks("hf4_struct_all")
pdf = h.compile("hf4_struct_all.typ")
norm = " ".join(h.text(pdf).split())

expected = {
    "abstract": "РЕФЕРАТ",
    "introduction": "ВВЕДЕНИЕ",
    "conclusion": "ЗАКЛЮЧЕНИЕ",
    "terms": "ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ",
    "authors": "СПИСОК ИСПОЛНИТЕЛЕЙ",
}

for name, txt in expected.items():
    c.check(
        f"upper_{name}",
        txt in norm,
        f"нет прописного заголовка '{txt}' в:\n  {norm[:200]}",
    )

# Эти заголовки не должны нести номер раздела. Проверяем КООРДИНАТНО:
# слева от первого слова заголовка на ТОЙ ЖЕ строке не должно быть числа
# (плоский поиск ловил бы номер страницы из footer перед заголовком
# следующей страницы — это не номер раздела).
W = h.words(pdf)
firsts = {txt.split()[0] for txt in expected.values()}
numbered = False
for w in W:
    if w[5] in firsts:
        left_same_line = [u for u in W if u[0] == w[0] and abs(u[2] - w[2]) < 3
                          and u[3] <= w[1] and u[5].rstrip(".").isdigit()]
        if left_same_line:
            numbered = True
c.check(
    "none_numbered",
    not numbered,
    "один из структурных заголовков получил номер раздела (число слева на той же строке)",
)

c.done()
