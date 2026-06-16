"""hf1 красная строка ВОССТАНАВЛИВАЕТСЯ у абзаца сразу после структурного
элемента: списка, рисунка, таблицы, формулы. Каждый такой абзац начинается
с x0≈120.47 (1.25см от левого поля 85.04).

Это типичное место бага: show-rule на list/figure/table/eq может сбросить
set par(first-line-indent) или вставить элемент, после которого первая
строка теряет отступ.
"""
import helpers as h

c = h.Checks("hf1_redline_after_structures")
pdf = h.compile("hf1_redline_after_structures.typ")

REDLINE = 120.47
ws = [w for w in h.words(pdf) if w[2] < 760]

lines = {}
for w in ws:
    lines.setdefault((w[0], round(w[2] / 3) * 3), []).append(w)

starts = {}
for (pg, y), g in sorted(lines.items()):
    g = sorted(g, key=lambda t: t[1])
    txt = " ".join(t[5] for t in g)
    for tag in ("ALIST", "BLIST", "CFIG", "DTAB", "EEQ"):
        if txt.startswith(tag) and tag not in starts:
            starts[tag] = min(t[1] for t in g)

c.check("all_five_paragraphs_found",
        len(starts) == 5,
        f"нашли начала абзацев {sorted(starts)}, ждём ALIST/BLIST/CFIG/DTAB/EEQ")

labels = {
    "BLIST": "после списка",
    "CFIG": "после рисунка",
    "DTAB": "после таблицы",
    "EEQ": "после формулы",
}
for tag, where in labels.items():
    x0 = starts.get(tag)
    c.check(f"redline_{tag}",
            x0 is not None and abs(x0 - REDLINE) < 1.5,
            f"абзац {where}: x0={x0}, ждём {REDLINE} — красная строка НЕ "
            f"восстановлена (баг show-rule структурного элемента)")

c.done()
