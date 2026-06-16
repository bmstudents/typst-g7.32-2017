"""hf4_unnum_heading: ненумерованный_заголовок(содержание:, номер:) — комбо.

Сигнатура (gost732-2017/utils/heading.typ):
  ненумерованный_заголовок(содержание: по-умолчанию, номер: по-умолчанию)[…]
  -> unnumbered_heading(toc:, numbering:)

Инварианты:
  1. содержание: по-умолчанию (none)  -> заголовок ПОПАДАЕТ в TOC, тело по
     центру и БЕЗ номера.
  2. содержание: false                -> НЕ попадает в TOC.
  3. содержание: [текст]              -> в TOC попадает ИМЕННО этот текст
     (supplement), тело — своё.
  4. номер: 7                         -> номер 7 должен быть согласован
     между TOC и телом (а не TOC=7 / тело=1).

TOC находится на стр. 1 (рендерится первым); тела заголовков — дальше.
Разделяем «строки TOC» (страница 1) и «тела» (страницы > 1) по координате.
"""
import helpers as h

c = h.Checks("hf4_unnum_heading")
pdf = h.compile("hf4_unnum_heading.typ")

ws = h.words(pdf)
# TOC целиком на стр. 1 (содержание() с pagebreak у первого heading).
toc_words = [w[5] for w in ws if w[0] == 1]
toc_seq = " ".join(toc_words)
# Тела заголовков — на страницах > 1.
body_words = [w[5] for w in ws if w[0] > 1]
body_seq = " ".join(body_words)
all_seq = " ".join(w[5] for w in ws)

# 1. дефолт -> в TOC
c.check(
    "default_in_toc",
    "ЗГдефолт" in toc_seq,
    f"ненумерованный_заголовок по умолчанию не попал в TOC:\n  TOC: {toc_seq[:200]}",
)
# Тело дефолтного заголовка отрисовано прописными (upper[] в show-rule) и по
# центру (cx около центра текстовой области ~319pt). В TOC регистр исходный
# ('ЗГдефолт'), поэтому тело ищем по прописной форме 'ЗГДЕФОЛТ'.
hit = [w for w in ws if w[5] == "ЗГДЕФОЛТ"]
c.check(
    "default_body_centered_upper",
    bool(hit) and abs((hit[0][1] + hit[0][3]) / 2 - 318.9) < 25,
    f"тело дефолтного заголовка не прописное/не отцентровано: {hit}",
)

# 2. содержание: false -> НЕ в TOC, но тело присутствует
c.check(
    "false_not_in_toc",
    "ЗГскрыт" not in toc_seq,
    f"содержание: false всё равно попал в TOC:\n  TOC: {toc_seq[:200]}",
)
c.check(
    "false_body_present",
    "ЗГскрыт" in body_seq,
    f"тело заголовка содержание: false отсутствует:\n  body: {body_seq[:200]}",
)

# 3. содержание: [текст] -> в TOC именно supplement-текст
c.check(
    "supplement_label_in_toc",
    "СупплЛейбл" in toc_seq,
    f"кастомный supplement-текст не попал в TOC:\n  TOC: {toc_seq[:200]}",
)

# 4. номер: 7 -> номер согласован между TOC и телом.
# TOC показывает '7 ЗГномер'. Тело должно показывать тот же '7', а не '1'.
toc_has_7 = "7 ЗГномер" in toc_seq or ("7" in toc_words and "ЗГномер" in toc_seq)
body_seq_around = body_seq
# номер в теле непосредственно перед словом тела заголовка
body_num = None
bw = [w[5] for w in ws if w[0] > 1]
if "ЗГномер" in bw:
    i = bw.index("ЗГномер")
    if i > 0:
        body_num = bw[i - 1]
c.check(
    "forced_number_consistent",
    toc_has_7 and body_num == "7",
    "номер: 7 не согласован между TOC и телом — TOC использует переданную\n"
    "  функцию нумерации (=> '7'), а тело берёт счётчик heading через\n"
    "  counter(heading).display() в gost732-2017/styles/heading.typ:20\n"
    "  (=> '1'). Переданный номер в теле игнорируется.\n"
    f"  TOC: ...{toc_seq[:120]}...\n  номер в теле перед 'ЗГномер': {body_num!r}",
)

c.done()
