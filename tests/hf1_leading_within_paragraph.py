"""hf1 межстрочный интервал ВНУТРИ одного абзаца ≈1.06em (≈14.84pt ведущий),
а НЕ полуторный. Дополнительно: шаг базовых линий равномерный по всему абзацу.

Шаг базовых линий (pitch) = leading + естественная высота строки Times 14pt.
Замерено: естественный шаг при leading=0 ≈9.26pt. Тогда ведущий = pitch-9.26.
1.06em*14pt = 14.84pt → pitch ≈ 24.1pt. Полуторный дал бы pitch ≈ 31pt.
"""
import helpers as h

c = h.Checks("hf1_leading_within_paragraph")
pdf = h.compile("hf1_leading_within_paragraph.typ")

ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 760]
ys = sorted(set(round(w[2], 2) for w in ws))

c.check("at_least_five_lines", len(ys) >= 5,
        f"строк {len(ys)}, нужно >=5 для надёжного измерения интервала")

pitches = [round(ys[i + 1] - ys[i], 3) for i in range(len(ys) - 1)]

NATURAL = 9.26
TARGET_PITCH = NATURAL + 1.06 * 14.0   # 24.10pt

# Все шаги равны целевому (равномерный интервал, без сбоев).
ok_pitch = [p for p in pitches if abs(p - TARGET_PITCH) < 1.0]
c.check("pitch_1_06em_all_lines",
        len(ok_pitch) == len(pitches),
        f"шаги базовых линий {pitches}, ждём все ≈{TARGET_PITCH:.2f} (1.06em)")

# НЕ полуторный (для 1.5 ведущий ~21pt → pitch ~30pt).
c.check("not_one_and_half",
        all(p < 28 for p in pitches),
        f"шаг {max(pitches):.2f}pt похож на полуторный интервал, а не 1.06em")

# Равномерность: разброс шагов мал.
spread = max(pitches) - min(pitches)
c.check("pitch_uniform",
        spread < 0.5,
        f"разброс шагов {spread:.3f}pt, ждём <0.5 (равномерный интервал)")

c.done()
