"""hd6: сквозная нумерация источников и согласованность [N] ↔ «N.».

hd6_refs.yml содержит 12 источников (full: true — печатаются все).
Инварианты ГОСТ 7.32-2017 / gost-r-705-2008-numeric:
  * заголовок «СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ»;
  * нумерация записей сквозная 1..12, БЕЗ пропусков, двузначные «10. 11. 12.»;
  * номер цитаты [N] в тексте равен номеру записи «N.» в списке;
  * порядок нумерации — по первому упоминанию (citation order):
    src02→[1], src03→[2], src01→[3], src10→[4], src11→[5], src12→[6].
"""
import re
import helpers as h

c = h.Checks("hd6_bib_numbering")
pdf = h.compile("hd6_bib_numbering.typ")
t = " ".join(h.text(pdf).split())

c.check("heading", "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ" in t,
        f"нет заголовка списка:\n{t[:400]}")

# Все 12 номеров записей присутствуют в виде «N.» (включая двузначные).
list_part = t.split("СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ", 1)[-1]
nums = [int(n) for n in re.findall(r"(?<!\d)(\d{1,2})\.\s", list_part)]
# Берём первые 12 уникальных по возрастанию — это и есть нумерация записей.
seen = []
for n in nums:
    if n not in seen:
        seen.append(n)
c.check("twelve_sequential", seen[:12] == list(range(1, 13)),
        f"нумерация записей не 1..12 подряд: {seen[:14]}")

c.check("two_digit_present", all(f"{k}." in list_part for k in (10, 11, 12)),
        f"нет двузначных номеров 10./11./12. в списке:\n{list_part[:600]}")

# Сопоставление: автор источника -> ожидаемый номер по citation order.
# src02 Петров=[1], src03 Сидоров=[2], src01 Иванов=[3],
# src10 Морозов=[4], src11 Зайцев=[5], src12 Павлов=[6].
expect = {"Петров": 1, "Сидоров": 2, "Иванов": 3,
          "Морозов": 4, "Зайцев": 5, "Павлов": 6}
ok = True
detail = []
for au, num in expect.items():
    m = re.search(r"(\d+)\.\s*" + au, t)
    got = int(m.group(1)) if m else None
    if got != num:
        ok = False
        detail.append(f"{au}: список#={got}, ожидался {num}")
c.check("citation_order_numbering", ok,
        "номера записей не совпали с порядком первого упоминания: " + "; ".join(detail))

# [N] в тексте: первые шесть цитат должны идти 1,2,3,4,5,6.
tokens = re.findall(r"\[(\d+)\]", t)
c.check("inline_tokens_order", tokens[:6] == ["1", "2", "3", "4", "5", "6"],
        f"номера цитат в тексте {tokens[:6]}, ожидались ['1','2','3','4','5','6']")
c.done()
