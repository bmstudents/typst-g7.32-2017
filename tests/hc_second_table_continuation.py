"""Номер в «Продолжение таблицы N» совпадает с номером самой таблицы.

Документ: короткая «Таблица 1» + длинная «Таблица 2» (переносится). Её
продолжение обязано быть «Продолжение таблицы 2» — не 1 (счётчик не отстал)
и не 3 (не убежал)."""
import re
import helpers as h

c = h.Checks("hc_second_table_continuation")
pdf = h.compile("hc_second_table_continuation.typ")
norm = " ".join(h.text(pdf).split())

c.check("table1_present", "Таблица 1" in norm, "нет «Таблица 1»")
c.check("table2_present", "Таблица 2" in norm, "нет «Таблица 2»")
conts = re.findall(r"Продолжение таблицы (\d+)", norm)
c.check("continuation_exists", len(conts) >= 1, f"нет продолжения: {norm[:200]}")
c.check("continuation_number_is_2", all(n == "2" for n in conts),
        f"номер продолжения != 2: {conts} (должно совпадать с «Таблица 2»)")
c.check("no_wrong_continuation_1", "Продолжение таблицы 1" not in norm,
        "ложное «Продолжение таблицы 1» (счётчик отстал)")
c.done()
