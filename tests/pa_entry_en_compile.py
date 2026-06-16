"""pa_entry-en: #show: gost732-2017 (английское имя) компилируется и рендерит
тот же базовый текст, что и русское имя."""
import helpers as h

c = h.Checks("pa_entry_en_compile")
pdf = h.compile("pa_entry_en_compile.typ")
t = h.text(pdf)

c.check("has_page", h.page_count(pdf) >= 1, "ни одной страницы")
c.check("body_rendered", "базовый абзац" in t, f"нет тела абзаца в:\n{t[:200]!r}")
c.check("second_line_rendered", "Вторая строка" in t,
        f"нет второй строки в:\n{t[:200]!r}")
c.done()
