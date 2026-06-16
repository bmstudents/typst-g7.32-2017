"""hd5 (контроль): двузначные номера разделов и подразделов.

Инварианты:
- разделы доходят до 10, 11, 12 (не «9, 9, 9» и не «1, 1, …»);
- 10-й подраздел первого раздела — '1.10' (а не '1.1' + '0');
- при переходе к Р2 вторая цифра сбрасывается: П2.1.
Должен ПРОХОДИТЬ.
"""
import re
import helpers as h

c = h.Checks("hd5_two_digit_sections")
pdf = h.compile("hd5_two_digit_sections.typ")
t = h.text(pdf)
norm = re.sub(r"[ \t]+", " ", t)


def num_of(label):
    m = re.search(r"([\d.]+) " + re.escape(label) + r"\b", norm)
    return m.group(1).rstrip(".") if m else None


c.check("sub_1_10",
        num_of("П1.10") == "1.10",
        f"десятый подраздел = {num_of('П1.10')}, ожидался 1.10")

c.check("section_2_resets_second_digit",
        num_of("П2.1") == "2.1",
        f"первый подраздел Р2 = {num_of('П2.1')}, ожидался 2.1")

c.check("sections_reach_two_digits",
        num_of("Р10") == "10" and num_of("Р11") == "11" and num_of("Р12") == "12",
        f"двузначные разделы: Р10={num_of('Р10')}, Р11={num_of('Р11')}, "
        f"Р12={num_of('Р12')}; ожидались 10,11,12")

# Полная последовательность 1..12 у всех разделов.
seq = [int(num_of(f"Р{i}")) if num_of(f"Р{i}") and num_of(f"Р{i}").isdigit() else None
       for i in range(1, 13)]
c.check("sections_full_sequence",
        seq == list(range(1, 13)),
        f"последовательность разделов {seq}, ожидалась 1..12")

c.done()
