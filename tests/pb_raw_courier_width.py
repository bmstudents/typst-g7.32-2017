"""pb raw-courier: ширина токена в листинге пропорциональна числу символов
(моноширинность). 'WWWW' и 'iiii' одинаковой ширины, 'Wi' — половина, '........' — вдвое."""
import helpers as h

c = h.Checks("pb_raw_courier_width")
pdf = h.compile("pb_raw_courier_width.typ")
ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 700]


def width(tok):
    hit = [w for w in ws if w[5] == tok]
    return (hit[0][3] - hit[0][1]) if hit else None


w4W = width("WWWW")
w4i = width("iiii")
w2 = width("Wi")
w8 = width("........")

c.check("found_all",
        None not in (w4W, w4i, w2, w8),
        f"не все токены найдены: WWWW={w4W} iiii={w4i} Wi={w2} dots={w8}")

if None not in (w4W, w4i, w2, w8):
    # W и i одинаковой ширины — главный признак моноширинного шрифта.
    c.check("W_equals_i_width",
            abs(w4W - w4i) < 0.5,
            f"'WWWW'={w4W:.2f} != 'iiii'={w4i:.2f} — шрифт пропорциональный, не моно")

    # Шаг на символ постоянен: 4 символа = 2 символа * 2 = 8/2 символов.
    per_char = w4W / 4
    c.check("char_step_constant",
            abs(w2 / 2 - per_char) < 0.2 and abs(w8 / 8 - per_char) < 0.2,
            f"шаг на символ непостоянен: 4ch->{per_char:.3f} 2ch->{w2/2:.3f} 8ch->{w8/8:.3f}")

c.done()
