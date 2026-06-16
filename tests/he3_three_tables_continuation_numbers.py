"""he3_three_tables_continuation_numbers: три длинные таблицы подряд, каждая
переносится через границу.

Общий счётчик counter("continuation") и сброс в конце каждой таблицы не
должны «склеивать» таблицы. Инварианты:
1. Ровно три подписи: «Таблица 1», «Таблица 2», «Таблица 3».
2. Первая физическая страница каждой таблицы несёт ПОДПИСЬ (не
   «Продолжение») — сброс continuation сработал между таблицами.
3. Все номера в «Продолжение таблицы N» принадлежат множеству {1,2,3} и
   идут неубывающе (1.. затем 2.. затем 3..) — номера не перепутаны."""
import re
import helpers as h

c = h.Checks("he3_three_tables_continuation_numbers")
pdf = h.compile("he3_three_tables_continuation_numbers.typ")
t = " ".join(h.text(pdf).split())

caps = re.findall(r"Таблица\s*([0-9]+)", t)
c.check("three_captions",
        caps == ["1", "2", "3"],
        f"подписи таблиц не 1/2/3: {caps}")

conts = [int(x) for x in re.findall(r"Продолжение таблицы\s*([0-9]+)", t)]
c.check("cont_numbers_in_set",
        conts and all(x in (1, 2, 3) for x in conts),
        f"номера продолжений вне множества 1..3: {conts}")

# Номера продолжений неубывающие (порядок таблиц сохранён, нет «скачка
# назад», т.е. continuation первой таблицы не утёк во вторую с её номером).
c.check("cont_numbers_monotonic",
        conts == sorted(conts),
        f"номера продолжений не монотонны (таблицы перепутаны): {conts}")

# Каждая таблица реально продолжается хотя бы раз (по построению длинные).
c.check("all_three_continue",
        set(conts) == {1, 2, 3},
        f"не все три таблицы продолжились: продолжения у таблиц {sorted(set(conts))}")

c.done()
