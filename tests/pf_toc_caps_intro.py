"""pf_toc_caps_intro: структурный заголовок 'Введение' выводится в оглавлении КАПСОМ (ВВЕДЕНИЕ)."""
import helpers as h

c = h.Checks("pf_toc_caps_intro")
pdf = h.compile("pf_toc_caps_intro.typ")
t = h.text(pdf)

# В оглавлении (и документе) — капс 'ВВЕДЕНИЕ', а не 'Введение'.
c.check("upper_in_text", "ВВЕДЕНИЕ" in t, f"нет капс 'ВВЕДЕНИЕ' в тексте:\n{t[:160]!r}")

# На странице оглавления присутствует слово 'ВВЕДЕНИЕ' (запись), и НЕ 'Введение'.
toc_page = next(w[0] for w in h.words(pdf) if w[5] == "СОДЕРЖАНИЕ")
toc_words = [w[5] for w in h.words(pdf) if w[0] == toc_page]
c.check("upper_entry_on_toc", "ВВЕДЕНИЕ" in toc_words,
        f"в оглавлении нет записи 'ВВЕДЕНИЕ': {toc_words[:10]}")
c.check("no_titlecase_entry", "Введение" not in toc_words,
        f"в оглавлении запись не в капсе ('Введение'): {toc_words[:10]}")

c.done()
