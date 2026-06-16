"""pb par-leading: сам ведущий (leading) ≈14.84pt = 1.06em*14pt.
Шаг базовых линий = leading + естественный шаг строки Times 14pt (9.26pt при
leading=0), поэтому leading = pitch - 9.26."""
import helpers as h

c = h.Checks("pb_par_leading_value")
pdf = h.compile("pb_par_leading_value.typ")
ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 700]

ys = sorted(set(round(w[2], 2) for w in ws))
c.check("two_lines", len(ys) >= 2, f"нужно >=2 строк, yMins={ys}")

if len(ys) >= 2:
    pitch = ys[1] - ys[0]
    NATURAL = 9.26          # шаг строки Times 14pt при leading=0 (замерено)
    leading = pitch - NATURAL
    target = 1.06 * 14      # 14.84pt

    c.check("leading_1_06em",
            abs(leading - target) < 1.0,
            f"ведущий {leading:.2f}pt, ждём ~{target:.2f} (1.06em); шаг={pitch:.2f}")

    # Это полуторного интервала НЕ даёт (для 1.5 ведущий был бы ~21pt).
    c.check("not_one_and_half",
            leading < 18,
            f"ведущий {leading:.2f}pt похож на 1.5 интервал, а не 1.06em")

c.done()
