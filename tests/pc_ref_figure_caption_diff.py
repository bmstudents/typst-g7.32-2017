"""pc ref-number-only: подпись содержит 'Рисунок N', а ссылка @ — только номер; два рисунка → '1' и '2'."""
import re
import helpers as h

c = h.Checks("pc_ref_figure_caption_diff")
pdf = h.compile("pc_ref_figure_caption_diff.typ")
t = " ".join(h.text(pdf).split())

r1 = re.search(r"СС1\s+(.+?)\s+СС1К", t)
r2 = re.search(r"СС2\s+(.+?)\s+СС2К", t)
v1 = r1.group(1) if r1 else ""
v2 = r2.group(1) if r2 else ""

c.check("ref1_is_1", v1 == "1", f"первая ссылка {v1!r}, ждём '1'")
c.check("ref2_is_2", v2 == "2", f"вторая ссылка {v2!r}, ждём '2'")

# Слово 'Рисунок' присутствует в подписях, но НЕ внутри текста ссылок.
c.check("supplement_in_caption_only",
        "Рисунок" in t and "Рисунок" not in v1 and "Рисунок" not in v2,
        f"'Рисунок' просочилось в ссылку: v1={v1!r} v2={v2!r}")

c.done()
