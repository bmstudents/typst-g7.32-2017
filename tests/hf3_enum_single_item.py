"""hf3_enum_single_item: ИНВАРИАНТ — перечисление из одного пункта:
ровно один маркер «1)», маркер на отступе ≈1.25см от поля, окружающие
абзацы не съедены и идут отдельными строками. Базовый sanity-гард.
"""
import helpers as h

LEFT_MARGIN = 30 * 2.83464567
PAR_INDENT = 1.25 * 28.3464567
MARKER_X = LEFT_MARGIN + PAR_INDENT  # ~120.47

c = h.Checks("hf3_enum_single_item")
pdf = h.compile("hf3_enum_single_item.typ")
t = h.text(pdf)
W = h.words(pdf)

markers = [w for w in W if w[5].endswith(")") and w[5][:-1].isdigit()]
c.check("exactly_one_marker", len(markers) == 1 and markers[0][5] == "1)",
        f"ожидали ровно один маркер '1)', нашли {[m[5] for m in markers]}")

if markers:
    c.check("marker_indent", abs(markers[0][1] - MARKER_X) < 2.0,
            f"маркер '1)' x={markers[0][1]:.2f} не на отступе ≈{MARKER_X:.2f}")

c.check("surrounding_text_kept",
        "Перед" in t and "После" in t and "единственный" in t,
        f"окружающий текст/пункт пропал:\n{t!r}")

# Пункт и соседние абзацы на разных строках (3 различных y у этих слов).
def y_of(word):
    return next((w[2] for w in W if w[5] == word), None)

ys = [y_of("Перед"), y_of("единственный"), y_of("После")]
c.check("three_distinct_rows", None not in ys and len({round(y, 1) for y in ys}) == 3,
        f"абзацы и пункт не на отдельных строках: y={ys}")

c.done()
