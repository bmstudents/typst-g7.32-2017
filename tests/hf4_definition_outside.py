"""hf4_definition_outside: определение(...) БЕЗ раздела определений.

определение(текст_ссылки, текст_определения) (gost732-2017/utils/definitions.typ):
когда раздел определений НЕ отрисован, функция должна просто напечатать
текст_ссылки (ref_text) как обычный текст и НЕ падать — никакой ссылки/якоря,
т.к. цели нет.

Инвариант:
  - компиляция проходит (h.compile не бросает);
  - ref_text ('ЭВМ', 'ОЗУ') присутствует в тексте;
  - текст_определения (полная расшифровка) НЕ печатается в месте вызова.
"""
import helpers as h

c = h.Checks("hf4_definition_outside")
# Сам факт успешной компиляции — первый инвариант (иначе h.compile бросит).
pdf = h.compile("hf4_definition_outside.typ")
norm = " ".join(h.text(pdf).split())

c.check(
    "ref_text_printed",
    "ЭВМ" in norm and "ОЗУ" in norm,
    f"ref_text не напечатан вне раздела определений:\n  {norm[:200]}",
)
c.check(
    "definition_text_not_inlined",
    "электронно-вычислительная" not in norm
    and "оперативное запоминающее" not in norm,
    "полная расшифровка термина напечатана в месте вызова (ожидался только\n"
    f"  ref_text):\n  {norm[:240]}",
)
# окружающий текст уцелел
c.check(
    "surrounding_text_intact",
    "Перед" in norm and "после" in norm,
    f"окружающий текст повреждён:\n  {norm[:200]}",
)

c.done()
