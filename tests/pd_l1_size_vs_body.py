"""pd l1-bold-size: высота глифов заголовка не меньше тела (заголовок >= тело).

Оба 14pt, но заголовок жирный — высота строки заголовка должна быть >= высоты
строки тела (не мельче). Сравниваем yMax-yMin слова заголовка и слова тела.
"""
import helpers as h

c = h.Checks("pd_l1_size_vs_body")
pdf = h.compile("pd_l1_size_vs_body.typ")
ws = [w for w in h.words(pdf) if w[0] == 1]

head = [w for w in ws if w[5] == "Методология"]
# тело: слово 'исследования' встречается только в абзаце
body = [w for w in ws if w[5] == "исследования"]

c.check("heading_present", len(head) >= 1, f"нет слова 'Методология': {head}")
c.check("body_present", len(body) >= 1, f"нет слова тела 'исследования': {body}")

if head and body:
    hh = head[0][4] - head[0][2]
    bh = body[0][4] - body[0][2]
    c.check("heading_not_smaller",
            hh >= bh - 0.5,
            f"высота заголовка {hh:.2f} меньше тела {bh:.2f} — заголовок мельче")
else:
    c.check("heading_not_smaller", False, "нет слов для сравнения высот")

c.done()
