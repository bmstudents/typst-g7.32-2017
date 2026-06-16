"""pe_struct_not_in_toc: структурный элемент 'Реферат' НЕ попадает в оглавление,
а обычный раздел — попадает. Проверяем по словам на странице оглавления (page 1)."""
import helpers as h

c = h.Checks("pe_struct_not_in_toc")
pdf = h.compile("pe_struct_not_in_toc.typ")

# Слова страницы оглавления (содержание() рендерится первым → page 1).
toc_page_words = [w[5] for w in h.words(pdf) if w[0] == 1]
toc_text = " ".join(toc_page_words)

# Заголовок оглавления на месте.
c.check("toc_heading_present", "СОДЕРЖАНИЕ" in toc_text,
        f"нет 'СОДЕРЖАНИЕ' на странице оглавления: {toc_text!r}")

# Обычный раздел присутствует в оглавлении.
c.check("normal_section_in_toc",
        "Обычный" in toc_page_words and "раздел" in toc_page_words,
        f"обычный раздел не найден в оглавлении: {toc_text!r}")

# 'Реферат' (в любом регистре) НЕ должен быть записью оглавления.
upper = toc_text.upper()
c.check("abstract_not_in_toc", "РЕФЕРАТ" not in upper,
        f"'Реферат' ошибочно попал в оглавление: {toc_text!r}")
c.done()
