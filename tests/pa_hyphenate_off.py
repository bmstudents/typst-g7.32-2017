"""pa_flag-hyphenate-off: фича-переносы-слов=нет → длинное слово в узком #box
НЕ разрывается переносом. В текстовом слое слово остаётся ЦЕЛЫМ на одной
строке, мягкого переноса (U+00AD) нет, дефиса в конце строки нет."""
import helpers as h

c = h.Checks("pa_hyphenate_off")
pdf = h.compile("pa_hyphenate_off.typ")
t = h.text(pdf)

word = "электроэнцефалография"
# Строки с буквами (без номера страницы).
body_lines = [l.strip() for l in t.splitlines()
              if l.strip() and not l.strip().isdigit()]

c.check("word_whole_one_line", word in body_lines,
        f"слово не осталось целым на одной строке:\n{body_lines!r}")

# Мягкий перенос (U+00AD) — маркер выполненного переноса — отсутствует.
c.check("no_soft_hyphen", "­" not in t,
        f"найден мягкий перенос U+00AD (слово разорвано):\n{t!r}")

# Ни одна строка тела не заканчивается дефисом любого вида.
hyph = ("­", "‐", "-")
c.check("no_trailing_hyphen",
        not any(l.endswith(hyph) for l in body_lines),
        f"строка заканчивается дефисом (перенос):\n{body_lines!r}")
c.done()
