"""pa_flag-nonbreaking-on (аспект 2): связка размеров остаётся НЕРАЗРЫВНОЙ.
Все три цифры и оба знака × лежат на одной строке (один yMin) — pack в box()
не дал переноса между '8' и '×'. Проверяем функционально по координатам слов."""
import helpers as h

c = h.Checks("pa_nonbreaking_on_box")
pdf = h.compile("pa_nonbreaking_on_box.typ")
t = h.text(pdf)
ws = h.words(pdf)

c.check("has_times", "8×8×8" in t, f"нет '8×8×8':\n{t!r}")

# Слово '8×8×8' собрано pdftotext в один токен (не разорвано пробелом/строкой).
tokens = [w for w in ws if "×" in w[5]]
c.check("single_token", len(tokens) == 1 and tokens[0][5] == "8×8×8",
        f"связка разорвана на токены: {[w[5] for w in tokens]!r}")

# Все цифры связки на одной горизонтали (одинаковый yMin) — не перенесено.
if tokens:
    y = tokens[0][2]
    c.check("one_line", abs(tokens[0][4] - y) < 14.0,
            f"токен '8×8×8' имеет большую высоту (перенос?): yMin={y} yMax={tokens[0][4]}")
else:
    c.check("one_line", False, "токен с × не найден")
c.done()
