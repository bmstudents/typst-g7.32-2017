"""pc ref-number-only: @f1 в тексте печатает голый номер '1' без слова 'рисунок'/'Рисунок'."""
import re
import helpers as h

c = h.Checks("pc_ref_figure_number")
pdf = h.compile("pc_ref_figure_number.typ")
t = " ".join(h.text(pdf).split())

m = re.search(r"РЕФДО\s+(.+?)\s+РЕФПОСЛЕ", t)
ref = m.group(1) if m else ""

c.check("ref_is_bare_number", ref == "1",
        f"ссылка = {ref!r}, ожидалось '1'")

# Между маркерами не должно быть слова рисунок (ссылка = только номер).
c.check("ref_has_no_supplement_word",
        "рисунок" not in ref.lower(),
        f"в самой ссылке есть слово 'рисунок': {ref!r}")

# Прямо перед номером-ссылкой не должно стоять авто-вставленное 'Рисунок'
# (т.е. 'Рисунок 1' появляется только в подписи, не в ссылке).
c.check("no_supplement_before_ref",
        "рисунок РЕФДО 1" in t or re.search(r"РЕФДО 1 РЕФПОСЛЕ", t) is not None,
        f"ссылка не выглядит как голый номер в контексте: {t[:300]}")

c.done()
