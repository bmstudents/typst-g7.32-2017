"""hd6: смешанная сортировка кириллица+латиница + общий префикс ключа.

Десять определений. Проверяем устойчивые инварианты сортировки
(.sorted по кодпойнтам — латиница раньше кириллицы):

  * латинские термины (Apple, Mid, Zebra) идут блоком раньше кириллических;
  * внутри латиницы: Apple < Mid < Zebra;
  * внутри кириллицы: Арбуз < Банан < Кэш < Кэширование < Маска < Массив < Яблоко;
  * «Кэш» (короче) идёт раньше «Кэширование» (общий префикс — короткое раньше);
  * «Маска» раньше «Массив» (различие на 3-й букве: с < с... к<с);
  * все 10 терминов реально присутствуют в разделе.
"""
import helpers as h

c = h.Checks("hd6_def_mixed_sort")
pdf = h.compile("hd6_def_mixed_sort.typ")
t = " ".join(h.text(pdf).split())
sec = t.split("определениями.")[-1]

heads = ["Apple", "Mid", "Zebra", "Арбуз", "Банан",
         "Кэширование", "Кэш", "Маска", "Массив", "Яблоко"]
pos = {h_: sec.find(h_) for h_ in heads}

c.check("all_ten_present", all(p >= 0 for p in pos.values()),
        f"не все 10 терминов в разделе: {pos}\nраздел: {sec}")

# «Кэш» внутри «Кэширование» — ищем точные подстроки термина с тире.
pos_kesh = sec.find("Кэш — буфер")
pos_kesh_ing = sec.find("Кэширование — процесс")
c.check("kesh_before_keshirovanie", 0 <= pos_kesh < pos_kesh_ing,
        f"«Кэш» (поз {pos_kesh}) должен идти раньше «Кэширование» (поз {pos_kesh_ing})")

# Латиница раньше кириллицы блоком.
latin_max = max(pos["Apple"], pos["Mid"], pos["Zebra"])
cyr_min = min(pos["Арбуз"], pos["Банан"], pos["Маска"], pos["Массив"], pos["Яблоко"])
c.check("latin_block_before_cyrillic", latin_max < cyr_min,
        f"латиница не идёт блоком раньше кириллицы: lat_max={latin_max}, cyr_min={cyr_min}")

# Внутри латиницы.
c.check("latin_internal_order", pos["Apple"] < pos["Mid"] < pos["Zebra"],
        f"латиница не по алфавиту: Apple={pos['Apple']} Mid={pos['Mid']} Zebra={pos['Zebra']}")

# Маска раньше Массив (Ма-с-к vs Ма-с-с: к=U+043A < с=U+0441).
c.check("maska_before_massiv", pos["Маска"] < pos["Массив"],
        f"«Маска» ({pos['Маска']}) должна идти раньше «Массив» ({pos['Массив']})")
c.done()
