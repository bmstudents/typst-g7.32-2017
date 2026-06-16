"""pf_recog_appendix_letter_b: приложение с другой буквой ('ПРИЛОЖЕНИЕ Б') тоже распознаётся, не нумеруется как '2'."""
import helpers as h

c = h.Checks("pf_recog_appendix_letter_b")
pdf = h.compile("pf_recog_appendix_letter_b.typ")
t = h.text(pdf)

# Обычный раздел получает '1'.
c.check("section_numbered_1", "1 Раздел один" in t, "раздел не получил '1'")

# Приложение Б распознано: запись 'ПРИЛОЖЕНИЕ Б', без числового номера '2'.
c.check("appendix_entry_present", "ПРИЛОЖЕНИЕ Б" in t,
        f"нет записи 'ПРИЛОЖЕНИЕ Б':\n{t[:160]!r}")
c.check("appendix_not_numbered_2", "2 ПРИЛОЖЕНИЕ" not in t and "2 Приложение" not in t,
        "приложение получило числовой номер '2'")

# Нумерация обычных разделов не продолжилась на приложение: '2 Раздел' не появляется.
c.check("no_section_2", "2 Раздел" not in t, "появился ложный '2 Раздел'")

c.done()
