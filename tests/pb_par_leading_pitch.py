"""pb par-leading: шаг базовых линий соседних строк абзаца постоянен и равен
≈24.1pt (1.06em-ведущий 14.84 + высота строки 9.26 для Times 14pt)."""
import helpers as h

c = h.Checks("pb_par_leading_pitch")
pdf = h.compile("pb_par_leading_pitch.typ")
ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 700]

ys = sorted(set(round(w[2], 2) for w in ws))
pitches = [round(ys[i + 1] - ys[i], 3) for i in range(len(ys) - 1)]

c.check("has_multiple_lines",
        len(pitches) >= 2,
        f"мало строк для замера шага: yMins={ys}")

c.check("pitch_24_1",
        len(pitches) >= 1 and all(abs(p - 24.1) < 1.5 for p in pitches),
        f"шаг строк {pitches}, ждём ~24.1pt")

# Шаг одинаков между всеми парами строк (разброс < 0.5pt).
c.check("pitch_constant",
        len(pitches) >= 2 and (max(pitches) - min(pitches)) < 0.5,
        f"шаг строк непостоянен: {pitches}")

c.done()
