"""pf_toc_caps_conclusion: структурный 'Заключение' в оглавлении капсом; обычный раздел НЕ капсом."""
import helpers as h

c = h.Checks("pf_toc_caps_conclusion")
pdf = h.compile("pf_toc_caps_conclusion.typ")

toc_page = next(w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ")
toc_words = [w[5] for w in h.words(pdf) if w[0] == toc_page]

# Структурный 'Заключение' — капсом.
c.check("conclusion_upper", "ЗАКЛЮЧЕНИЕ" in toc_words,
        f"нет капс записи 'ЗАКЛЮЧЕНИЕ' в оглавлении: {toc_words[:12]}")
c.check("conclusion_not_titlecase", "Заключение" not in toc_words,
        f"запись заключения не в капсе: {toc_words[:12]}")

# Обычный раздел НЕ капсуется в оглавлении (остаётся 'Раздел', а не 'РАЗДЕЛ').
c.check("normal_section_not_upper", "Раздел" in toc_words and "РАЗДЕЛ" not in toc_words,
        f"обычный раздел неверно капсован: {toc_words[:12]}")

c.done()
