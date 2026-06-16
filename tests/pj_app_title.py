"""pj 1: приложение с буква:"А" -> 'ПРИЛОЖЕНИЕ А' в тексте."""
import helpers as h

c = h.Checks("pj_app_title")
pdf = h.compile("pj_app_title.typ")
t = " ".join(h.text(pdf).split())

c.check("title_phrase", "ПРИЛОЖЕНИЕ А" in t,
        f"нет 'ПРИЛОЖЕНИЕ А' в:\n{t[:200]}")
c.check("title_upper", "Приложение А" not in t.replace("ПРИЛОЖЕНИЕ", "ПРИЛОЖЕНИЕ"),
        "заголовок не приведён к верхнему регистру (есть 'Приложение А')")
c.check("letter_present", " А " in (" " + t + " ") or "ПРИЛОЖЕНИЕ А" in t,
        f"буква 'А' не отображена")
c.done()
