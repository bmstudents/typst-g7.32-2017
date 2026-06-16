"""hf1 заголовок раздела НЕ должен выключаться по ширине (justify).

ГОСТ 7.32-2017: заголовки печатаются без растяжения межсловных пробелов.
Многострочный заголовок раздела не должен иметь первую строку, дотянутую до
правого края текстового поля за счёт раздутых межсловных пробелов — это
ошибка выключки заголовка.

ПРИЧИНА (файл пакета): gost732-2017/styles/heading.typ, show heading: тело
заголовка оборачивается в par(..., justify: true). justify:true заставляет
первую (неполную) строку многострочного заголовка растягиваться на всю
ширину блока, раздувая пробелы (≈12.9pt против естественных ≈3.5pt).

Тест проверяет два независимых инварианта строки заголовка:
  1) первая строка заголовка НЕ дотянута до правого края (xMax < ~552);
  2) межсловные пробелы в заголовке близки к естественным (а не раздуты).
"""
import helpers as h

c = h.Checks("hf1_heading_not_justified")
pdf = h.compile("hf1_heading_not_justified.typ")

RIGHT = 552.76
ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 760]

lines = {}
for w in ws:
    lines.setdefault(round(w[2] / 3) * 3, []).append(w)

rows = []
for y, g in sorted(lines.items()):
    g = sorted(g, key=lambda t: t[1])
    rows.append((y, g))

# Естественный межсловный пробел — из строк тела абзаца (НЕ заголовок).
# Берём строку, начинающуюся со слова "Обычный" или её продолжение.
def gaps(g):
    return [g[i + 1][1] - g[i][3] for i in range(len(g) - 1)]

# Заголовок — первая строка (содержит цифру "1" + "Очень"). Это многострочный
# заголовок: его первая строка неполная и НЕ должна растягиваться.
head_line = rows[0][1]
head_text = " ".join(w[5] for w in head_line)
head_xmax = max(w[3] for w in head_line)
head_gaps = gaps(head_line)

c.check("heading_multiline",
        len(rows) >= 2 and head_text[0].isdigit(),
        f"первая строка должна быть началом многострочного заголовка: «{head_text}»")

# Естественный пробел: возьмём строку тела (есть слово 'для'/'нужен'/'сравнения'
# или начинается с 'Обычный').
body_gaps = []
for y, g in rows[1:]:
    txt = " ".join(w[5] for w in g)
    if any(k in txt for k in ("сравнения", "нужен", "естественного", "после")):
        body_gaps = gaps(g)
        break
nat = min(body_gaps) if body_gaps else 3.5

c.check("have_natural_gap_reference", len(body_gaps) >= 2,
        f"не нашли строку тела для эталонного пробела (нашёл {body_gaps})")

# 1) Заголовок не дотянут до правого края.
c.check("heading_first_line_not_flush_right",
        head_xmax < RIGHT - 5,
        f"первая строка заголовка дотянута до xMax={head_xmax:.2f} (≈{RIGHT}). "
        f"Заголовок выключен по ширине — justify:true в styles/heading.typ "
        f"(par-обёртка тела заголовка). Заголовки по ГОСТ не выключаются.")

# 2) Межсловные пробелы заголовка не раздуты относительно естественного.
if head_gaps and body_gaps:
    max_hgap = max(head_gaps)
    c.check("heading_word_spacing_not_stretched",
            max_hgap < nat * 2.0,
            f"межсловный пробел в заголовке {max_hgap:.2f}pt против естественного "
            f"{nat:.2f}pt (раздут в {max_hgap/nat:.1f}×). Заголовок растягивается "
            f"выключкой — баг justify в styles/heading.typ")

c.done()
