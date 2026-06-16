"""pc page-justify: выключка действует на оба абзаца — большинство строк прижато к ≈552."""
import helpers as h

c = h.Checks("pc_justify_two_paras")
pdf = h.compile("pc_justify_two_paras.typ")
right_edge = 552.76

ws = sorted((w for w in h.words(pdf) if w[0] == 1), key=lambda t: round(t[2]))
foot_y = max(w[2] for w in ws)
lines = {}
for w in ws:
    if w[2] > foot_y - 5:        # пропускаем футер
        continue
    lines.setdefault(round(w[2] / 3) * 3, []).append(w)

line_rights = [max(g, key=lambda t: t[3])[3] for g in lines.values()]
c.check("enough_lines", len(line_rights) >= 4,
        f"строк {len(line_rights)}, нужно >=4 (два многострочных абзаца)")

# Две последние строки — концы абзацев (могут быть короче). Остальные ровные.
flush = [r for r in line_rights if abs(r - right_edge) < 3]
c.check("majority_flush_right",
        len(flush) >= len(line_rights) - 2,
        f"к правому краю прижаты {len(flush)} из {len(line_rights)} строк; края={[round(r,1) for r in sorted(line_rights)]}")

c.done()
