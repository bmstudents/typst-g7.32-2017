"""pk: #определение(...) в тексте выводит текст-ссылки на месте."""
import helpers as h

c = h.Checks("pk_def_inline_renders")
pdf = h.compile("pk_def_inline_renders.typ")
t = " ".join(h.text(pdf).split())

# Текст-ссылки ("ОЗУ") должен появиться в теле абзаца.
c.check("ref_text_present", "ОЗУ" in t,
        f"нет текста-ссылки 'ОЗУ' в:\n{t[:300]}")

# Ссылка встроена в окружающий текст (слово до и слово после на месте).
c.check("inline_context", "среди которых ОЗУ играет" in t,
        f"текст-ссылки не встроен в абзац:\n{t[:300]}")
c.done()
