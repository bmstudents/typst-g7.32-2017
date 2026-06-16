"""h1 ТАБЛИЦЫ #4 — ШИРОКАЯ ТАБЛИЦА (1fr,1fr) НА ВСЮ ШИРИНУ ПОЛЯ.

Полоса набора: левое поле x≈85.04, правый край≈552.76. С учётом inset=10pt
содержимое крайних ячеек должно стоять у x≈95 слева и x≈542.76 справа.
Берём левое выравнивание в левой колонке и правое в правой — тогда текст
прижат к границам тела, и по нему точно измеряется ширина таблицы.

Измеримые инварианты:
  1) левый край тела ≈ 85+inset (текст левой колонки x0 ≈ 95, ±3pt);
  2) правый край тела ≈ 552.76−inset (текст правой колонки x1 ≈ 542.76, ±3pt);
  3) тело занимает почти всю полосу (ширина блока > 90% от 467.7pt).

Этот тест — КОНТРАСТ к #1/#2/#6: при ЯВНЫХ (1fr,1fr) Typst растягивает
таблицу на полосу, и центрирование figure не сжимает её. Если тест упадёт —
сломалось и full-width-поведение.
"""
import helpers as h

c = h.Checks("h1_wide_table_fullwidth")
pdf = h.compile("h1_wide_table_fullwidth.typ")
ws = [w for w in h.words(pdf) if w[0] == 1 and 95 < w[2] < 700]

LEFT, RIGHT, INSET = 85.04, 552.76, 10.0
exp_left = LEFT + INSET     # ≈ 95.04
exp_right = RIGHT - INSET    # ≈ 542.76
polosa = RIGHT - LEFT        # ≈ 467.72

body = [w for w in ws if w[5] in ("Левая", "Правая", "нл", "нп")]
c.check("body_present", len(body) >= 3,
        f"тело широкой таблицы не найдено: {[(w[5], round(w[1])) for w in ws]}")

if body:
    body_x0 = min(w[1] for w in body)
    body_x1 = max(w[3] for w in body)
    width = body_x1 - body_x0

    c.check(
        "left_edge_at_margin",
        abs(body_x0 - exp_left) <= 3,
        f"левый край тела x0={body_x0:.2f}, ждём ≈{exp_left:.2f} (поле+инсет), "
        f"Δ={body_x0 - exp_left:+.2f}pt.",
    )
    c.check(
        "right_edge_at_margin",
        abs(body_x1 - exp_right) <= 3,
        f"правый край тела x1={body_x1:.2f}, ждём ≈{exp_right:.2f} "
        f"(правое поле−инсет), Δ={body_x1 - exp_right:+.2f}pt — таблица не на всю ширину.",
    )
    c.check(
        "spans_full_polosa",
        width > 0.90 * polosa,
        f"ширина тела {width:.2f}pt < 90% полосы ({0.90 * polosa:.2f}); "
        f"таблица не растянута на всю полосу набора {polosa:.2f}pt.",
    )

c.done()
