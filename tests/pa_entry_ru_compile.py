"""pa_entry-ru: #show: гост732-2017 компилируется, базовый текст рендерится."""
import helpers as h

c = h.Checks("pa_entry_ru_compile")
pdf = h.compile("pa_entry_ru_compile.typ")
t = h.text(pdf)

c.check("has_page", h.page_count(pdf) >= 1, "ни одной страницы")
c.check("body_rendered", "базовый абзац" in t, f"нет тела абзаца в:\n{t[:200]!r}")
c.check("second_line_rendered", "Вторая строка" in t,
        f"нет второй строки в:\n{t[:200]!r}")
c.done()
