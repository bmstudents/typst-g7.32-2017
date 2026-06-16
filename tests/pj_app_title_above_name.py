"""pj 3: 'ПРИЛОЖЕНИЕ А' выше названия (y заголовка < y названия)."""
import helpers as h

c = h.Checks("pj_app_title_above_name")
pdf = h.compile("pj_app_title_above_name.typ")
t = " ".join(h.text(pdf).split())

c.check("both_present", "ПРИЛОЖЕНИЕ А" in t and "Техническое задание" in t,
        f"нет заголовка или названия в:\n{t[:300]}")

# Заголовок 'ПРИЛОЖЕНИЕ' и название 'Техническое' оба на стр.1; Y растёт вниз.
y_title = h.y_of(pdf, "ПРИЛОЖЕНИЕ", page=1)
y_name = h.y_of(pdf, "Техническое", page=1)
c.check("title_above_name",
        y_title is not None and y_name is not None and y_title < y_name,
        f"порядок неверен: title_y={y_title} name_y={y_name}")
c.done()
