"""hf3_list_enum_independence: ИНВАРИАНТ — каждый отдельный enum-блок нумеруется
с 1) заново, а вставленный между ними маркированный список не сбивает счётчик.

Рукописный show enum заводит локальную `let i = 1` на КАЖДЫЙ блок enum, поэтому
два разных перечисления должны независимо начинаться с 1). Проверяем, что:
  - оба enum дают ровно 1) и 2);
  - между ними два тире-маркера;
  - нет «утёкшего» счётчика (например 3) 4) во втором блоке).
"""
import helpers as h

c = h.Checks("hf3_list_enum_independence")
pdf = h.compile("hf3_list_enum_independence.typ")
W = h.words(pdf)

# Маркеры enum по порядку сверху вниз.
enum_markers = [w[5] for w in sorted(W, key=lambda t: (t[0], t[2]))
                if w[5].endswith(")") and w[5][:-1].isdigit()]
dashes = [w for w in W if w[5] == "–"]

c.check("two_enum_blocks_each_1_2", enum_markers == ["1)", "2)", "1)", "2)"],
        f"нумерация enum-блоков нарушена: {enum_markers} (ожидали 1)2)1)2))")

c.check("dashes_between", len(dashes) == 2,
        f"ожидали 2 тире-маркера между перечислениями, нашли {len(dashes)}")

# Второй enum действительно начинается с 1) (не продолжает 3)).
c.check("second_enum_restarts", enum_markers[2:] == ["1)", "2)"],
        f"второй enum не сбросился на 1): {enum_markers}")

c.done()
