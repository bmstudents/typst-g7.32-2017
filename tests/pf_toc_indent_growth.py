"""pf_toc_indent_growth: отступ записи монотонно растёт по уровням; шаг отступа примерно постоянен (>0)."""
import helpers as h

c = h.Checks("pf_toc_indent_growth")
pdf = h.compile("pf_toc_indent_growth.typ")
toc_page = next(w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ")
toc = [w for w in h.words(pdf) if w[0] == toc_page]


def x_of(label):
    hits = [w for w in toc if w[5] == label]
    return hits[0][1] if hits else None


# Левый край номера каждого уровня.
x1 = x_of("1")
x2 = x_of("1.1")
x3 = x_of("1.1.1")
c.check("levels_present", None not in (x1, x2, x3), f"x1={x1} x2={x2} x3={x3}")

if None not in (x1, x2, x3):
    d12 = x2 - x1
    d23 = x3 - x2
    c.check("positive_step_l1_l2", d12 > 1.0, f"шаг 1->1.1 не положителен: {d12:.2f}pt")
    c.check("positive_step_l2_l3", d23 > 1.0, f"шаг 1.1->1.1.1 не положителен: {d23:.2f}pt")
    # Шаг отступа на каждый уровень примерно одинаков (grid: 1em на уровень).
    c.check("step_consistent", abs(d12 - d23) < 6.0,
            f"шаг отступа непостоянен: d12={d12:.2f} d23={d23:.2f}")

c.done()
