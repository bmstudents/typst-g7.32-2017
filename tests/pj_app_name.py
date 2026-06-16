"""pj 2: содержание:[Техническое задание] -> название появляется."""
import helpers as h

c = h.Checks("pj_app_name")
pdf = h.compile("pj_app_name.typ")
t = " ".join(h.text(pdf).split())

c.check("name_present", "Техническое задание" in t,
        f"нет названия 'Техническое задание' в:\n{t[:300]}")
c.check("title_present", "ПРИЛОЖЕНИЕ А" in t,
        f"нет 'ПРИЛОЖЕНИЕ А' в:\n{t[:300]}")
c.done()
