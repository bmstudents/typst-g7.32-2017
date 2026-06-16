"""pd heading-sticky: пункт (уровень 3) у нижней границы уходит на след. страницу
вместе со своим первым словом текста — не остаётся висеть один."""
import helpers as h

c = h.Checks("pd_heading_sticky_point")
pdf = h.compile("pd_heading_sticky_point.typ")
ws = h.words(pdf)

def page_of(word):
    hits = [w for w in ws if w[5] == word]
    return hits[0][0] if hits else None

p_head = page_of("Пункт")
p_text = page_of("Содержательное")

c.check("heading_present", p_head is not None, "нет заголовка 'Пункт'")
c.check("text_present", p_text is not None, "нет первого слова текста 'Содержательное'")

c.check("same_page",
        p_head is not None and p_head == p_text,
        f"заголовок 'Пункт' на стр.{p_head}, текст на стр.{p_text} — заголовок завис")

c.done()
