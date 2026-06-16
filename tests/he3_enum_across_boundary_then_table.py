"""he3_enum_across_boundary_then_table: перечисление через границу страницы,
затем таблица с переносом.

Инварианты:
1. Перечисление пересекает границу (маркеры на >=2 страницах).
2. Нумерация сквозная и непрерывная: маркеры 1)..40) присутствуют все,
   ровно по разу, и НЕ рестартуют (нет второго «1)»).
3. Маркеры монотонно возрастают по порядку (page, y).
4. Идущая следом таблица переносится, продолжения с номером 1; хвост на
   месте."""
import re
import helpers as h

c = h.Checks("he3_enum_across_boundary_then_table")
pdf = h.compile("he3_enum_across_boundary_then_table.typ")
ws = h.words(pdf)

markers = [(w[0], w[2], int(w[5][:-1])) for w in ws
           if re.match(r"^[0-9]+\)$", w[5])]
nums = [m[2] for m in markers]

c.check("crosses_boundary",
        len({m[0] for m in markers}) >= 2,
        f"перечисление не пересекло границу: страницы маркеров "
        f"{sorted({m[0] for m in markers})}")

c.check("all_40_once",
        sorted(nums) == list(range(1, 41)),
        f"маркеры не 1..40 по разу (рестарт?): {sorted(nums)}")

# В порядке вёрстки (page, y) номера строго возрастают 1,2,3,...,40.
ordered = [m[2] for m in sorted(markers, key=lambda t: (t[0], t[1]))]
c.check("continuous_no_restart",
        ordered == list(range(1, 41)),
        f"нумерация не сквозная по порядку вёрстки: {ordered}")

t = " ".join(h.text(pdf).split())
conts = re.findall(r"Продолжение таблицы\s*([0-9]+)", t)
c.check("table_after_continues",
        conts and all(x == "1" for x in conts),
        f"таблица после перечисления не перенеслась корректно: {conts}")

c.check("tail_present",
        any(w[5] == "Хвостовой" for w in ws),
        "хвостовой текст потерян")

c.done()
