"""hf4_defsection_twice: раздел определений вызван дважды -> не должен падать.

Робастность: если пользователь по ошибке вставит
определения_обозначения_сокращения_раздел() дважды (или раздел попадёт в
шаблон + ручной вызов), пакет не должен ронять компиляцию.

Сейчас определение() при отрисованном разделе создаёт якорь
label('internal-definition-entry-<ключ>-0'); второй вызов раздела печатает
тот же якорь повторно -> typst падает с 'label occurs multiple times'.

Инвариант: компиляция проходит (h.compile не бросает). Тест ловит ошибку
компиляции и выдаёт детальный FAIL вместо краха харнесса.
"""
import helpers as h

c = h.Checks("hf4_defsection_twice")

ok = True
err = ""
pdf = None
try:
    pdf = h.compile("hf4_defsection_twice.typ")
except RuntimeError as e:
    ok = False
    err = str(e)

c.check(
    "compiles_without_dup_label",
    ok,
    "двойной вызов определения_обозначения_сокращения_раздел() роняет\n"
    "  компиляцию дублирующимся label. Источник:\n"
    "  gost732-2017/utils/definitions.typ — definition() вешает якорь\n"
    "  label('internal-definition-entry-<ключ>-0') при отрисованном разделе,\n"
    "  а второй вызов раздела печатает тот же label повторно.\n"
    f"  Ошибка typst:\n{err[:400]}",
)

if ok and pdf:
    norm = " ".join(h.text(pdf).split())
    c.check(
        "heading_present",
        "ОПРЕДЕЛЕНИЯ, ОБОЗНАЧЕНИЯ И СОКРАЩЕНИЯ" in norm,
        f"нет заголовка раздела определений:\n  {norm[:200]}",
    )

c.done()
