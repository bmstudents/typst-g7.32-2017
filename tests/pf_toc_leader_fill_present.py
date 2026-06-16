"""pf_toc_leader_fill_present: заполнитель (fill) присутствует даже для короткой записи — точки в текстовом слое."""
import helpers as h

c = h.Checks("pf_toc_leader_fill_present")
pdf = h.compile("pf_toc_leader_fill_present.typ")
t = h.text(pdf)

# В текстовом слое строки оглавления присутствует последовательность точек-заполнителей.
c.check("dot_run_in_text", ". . . . . ." in t or "......" in t,
        f"нет повторяющихся точек-заполнителей в тексте оглавления:\n{t[:200]!r}")

# И координатно: на строке записи 'Краткий' есть хотя бы несколько точек.
toc_page = next(w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ")
y = next(w[2] for w in h.words(pdf) if w[0] == toc_page and w[5] == "Краткий")
dots = [w for w in h.words(pdf) if w[0] == toc_page and abs(w[2] - y) < 1.0 and w[5] == "."]
c.check("dots_on_entry_line", len(dots) >= 5,
        f"мало точек на строке короткой записи: {len(dots)}")

c.done()
