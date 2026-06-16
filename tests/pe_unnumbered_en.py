"""pe_unnumbered_en: англ #unnumbered_heading(toc: [Имя])[Текст] компилируется;
текст появляется, имя попадает в оглавление."""
import helpers as h

c = h.Checks("pe_unnumbered_en")
pdf = h.compile("pe_unnumbered_en.typ")  # бросит при ошибке компиляции
norm = " ".join(h.text(pdf).split())

c.check("body_text", "UNNUMBERED BODY TEXT" in norm,
        f"нет текста ненумерованного заголовка (англ) в:\n{norm[:200]}")
c.check("toc_name", "TocCustomName" in norm,
        "имя из аргумента 'toc:' не появилось в оглавлении")
c.done()
