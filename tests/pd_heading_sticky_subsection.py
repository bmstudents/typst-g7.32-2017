"""pd heading-sticky: заголовок у нижней границы не висит один —
подраздел и его первое слово текста оказываются на одной странице."""
import helpers as h

c = h.Checks("pd_heading_sticky_subsection")
pdf = h.compile("pd_heading_sticky_subsection.typ")
ws = h.words(pdf)

def page_of(word):
    hits = [w for w in ws if w[5] == word]
    return hits[0][0] if hits else None

p_head = page_of("Подраздел")
p_first = page_of("Первое")

c.check("heading_present", p_head is not None, "нет заголовка 'Подраздел'")
c.check("body_present", p_first is not None, "нет первого слова текста 'Первое'")

c.check("heading_and_text_same_page",
        p_head is not None and p_head == p_first,
        f"заголовок на стр.{p_head}, первое слово текста на стр.{p_first} — "
        f"заголовок завис отдельно от текста")

# Заголовок не остался последним элементом на предыдущей странице.
if p_head is not None:
    head_y = h.y_of(pdf, "Подраздел", page=p_head)
    below = [w for w in ws if w[0] == p_head and w[2] > head_y + 1]
    c.check("text_follows_on_same_page",
            len(below) > 0,
            f"под заголовком на стр.{p_head} нет ни одного слова — заголовок одинок внизу")
else:
    c.check("text_follows_on_same_page", False, "нет заголовка")

c.done()
