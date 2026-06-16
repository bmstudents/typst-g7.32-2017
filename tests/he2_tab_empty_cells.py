"""he2 EDGE-таблицы #2: таблица с ПУСТЫМИ ячейками ([], [текст]).

ИНВАРИАНТЫ:
  1) компиляция не падает (compile бросит сама при ошибке);
  2) все непустые маркеры присутствуют: АА ВВ ГГ ДД ЕЕ;
  3) непустые ячейки стоят на 3 разных базовых линиях (3 строки) — пустые
     ячейки не «съели» строки и не сдвинули раскладку;
  4) колонок ровно 3: в каждой строке непустые слова стоят в разных x-полосах.

Файл пакета при провале: gost732-2017/styles/table.typ / styles/figure.typ.
"""
import helpers as h

c = h.Checks("he2_tab_empty_cells")
pdf = h.compile("he2_tab_empty_cells.typ")
t = h.text(pdf)
ws = h.words(pdf)

for m in ["АА", "ВВ", "ГГ", "ДД", "ЕЕ"]:
    c.check(f"present_{m}", m in t, f"нет маркера {m}:\n{t}")

cells = [w for w in ws if w[5] in {"АА", "ВВ", "ГГ", "ДД", "ЕЕ"} and w[0] == 1]
rows = sorted(set(round(w[2]) for w in cells))
c.check("three_rows", len(rows) == 3,
        f"непустые ячейки заняли {len(rows)} строк (ожидали 3): {rows} — "
        f"пустые ячейки сломали раскладку. Файл: gost732-2017/styles/figure.typ")

# в строке с ГГ единственный непустой — он в средней колонке (x между АА и ВВ)
x_aa = next((w[1] for w in cells if w[5] == "АА"), None)
x_bb = next((w[1] for w in cells if w[5] == "ВВ"), None)
x_gg = next((w[1] for w in cells if w[5] == "ГГ"), None)
ok_mid = (x_aa is not None and x_bb is not None and x_gg is not None
          and x_aa < x_gg < x_bb)
c.check("gg_in_middle_column", ok_mid,
        f"ГГ (средняя колонка) x={x_gg} не между АА={x_aa} и ВВ={x_bb} — "
        f"пустые ячейки сместили колонку. Файл: gost732-2017/styles/table.typ")
c.done()
