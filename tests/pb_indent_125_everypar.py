"""pb par-indent-125: красная строка ставится у КАЖДОГО абзаца (config all:true),
включая самый первый — первое слово каждого абзаца на x≈120.47."""
import helpers as h

c = h.Checks("pb_indent_125_everypar")
pdf = h.compile("pb_indent_125_everypar.typ")
ws = [w for w in h.words(pdf) if w[0] == 1 and w[2] < 700]

# По одной строке на абзац: левый край каждой строки = красная строка.
lines = {}
for w in ws:
    lines.setdefault(round(w[2]), []).append(w[1])
firsts = [min(xs) for _, xs in sorted(lines.items())]

c.check("three_paragraphs",
        len(firsts) == 3,
        f"ждём 3 абзаца-строки, нашли {len(firsts)}: {[round(x,1) for x in firsts]}")

c.check("all_indented_120",
        all(abs(x - 120.47) < 2 for x in firsts),
        f"не у всех абзацев красная строка: левые края={[round(x,2) for x in firsts]}, ждём ~120.47")

# В т.ч. первый абзац документа (часто его не отбивают) — тоже с отступом.
c.check("first_par_indented",
        len(firsts) > 0 and abs(firsts[0] - 120.47) < 2,
        f"первый абзац без красной строки: x={firsts[0]:.2f}" if firsts else "нет абзацев")

c.done()
