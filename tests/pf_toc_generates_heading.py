"""pf_toc_generates_heading: #содержание() печатает заголовок 'СОДЕРЖАНИЕ' первым на странице оглавления."""
import helpers as h

c = h.Checks("pf_toc_generates_heading")
pdf = h.compile("pf_toc_generates_heading.typ")
t = h.text(pdf)

# Заголовок оглавления присутствует.
c.check("heading_present", "СОДЕРЖАНИЕ" in t, f"нет 'СОДЕРЖАНИЕ' в тексте:\n{t[:150]!r}")

# 'СОДЕРЖАНИЕ' — самое верхнее слово первой страницы (это заголовок оглавления, а не запись).
fw = h.first_word(pdf, 1)
c.check("heading_is_topmost", fw is not None and fw[1] == "СОДЕРЖАНИЕ",
        f"первое слово страницы 1 не 'СОДЕРЖАНИЕ': {fw}")

# Заголовок оглавления отцентрован (xMin заметно больше левого поля ≈85).
toc_word = next((w for w in h.words(pdf) if w[0] == 1 and w[5] == "СОДЕРЖАНИЕ"), None)
c.check("heading_centered", toc_word is not None and toc_word[1] > 150,
        f"заголовок 'СОДЕРЖАНИЕ' не отцентрован: {toc_word}")

c.done()
