"""pd struct-upper: '= Введение' (смешанный регистр) -> в тексте КАПС 'ВВЕДЕНИЕ'."""
import helpers as h

c = h.Checks("pd_struct_upper_mixedcase")
pdf = h.compile("pd_struct_upper_mixedcase.typ")
t = h.text(pdf)

c.check("uppercased",
        "ВВЕДЕНИЕ" in t,
        f"нет капс-формы 'ВВЕДЕНИЕ' в:\n{t[:300]!r}")

# Исходная смешанная форма 'Введение' не должна остаться как самостоятельное
# слово заголовка (она апперкейзится). Тело может содержать слово 'введения',
# поэтому проверяем именно отсутствие точного 'Введение' как заголовка.
ws = h.words(pdf)
mixed_heading = [w for w in ws if w[5] == "Введение"]
c.check("not_mixed_case_heading",
        len(mixed_heading) == 0,
        f"остался не-апперкейзнутый заголовок 'Введение': {mixed_heading}")

c.done()
