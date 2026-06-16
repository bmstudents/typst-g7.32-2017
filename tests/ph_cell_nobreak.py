"""10 cell-nobreak: длинное слово в узкой колонке через ячейку() не переносится
по слогам — слово остаётся целым, в тексте нет дефиса-переноса."""
import helpers as h

c = h.Checks("ph_cell_nobreak")
pdf = h.compile("ph_cell_nobreak.typ")
t = h.text(pdf)

word = "Электроэнцефалографический"
c.check("word_intact", word in t,
        f"длинное слово разорвано переносом — целого '{word}' нет в:\n{t}")
# Дефиса-переноса (буква + '-' + перевод строки/буква) быть не должно.
c.check("no_soft_hyphen", "-\n" not in t and "­" not in t,
        f"найден перенос по слогам (мягкий дефис/'-\\n') в:\n{t!r}")
c.done()
