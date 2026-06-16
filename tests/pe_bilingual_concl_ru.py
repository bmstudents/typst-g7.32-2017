"""pe_bilingual_concl_ru: рус #заключение и англ #conslusion (опечатка в пакете)
дают одинаковый заголовок 'ЗАКЛЮЧЕНИЕ'. Сравниваем нормализованный текст целиком."""
import helpers as h

c = h.Checks("pe_bilingual_concl_ru")
ru = " ".join(h.text(h.compile("pe_bilingual_concl_ru.typ")).split())
en = " ".join(h.text(h.compile("pe_bilingual_concl_en.typ")).split())

c.check("ru_has_heading", "ЗАКЛЮЧЕНИЕ" in ru, f"нет 'ЗАКЛЮЧЕНИЕ' в рус: {ru[:120]!r}")
c.check("en_has_heading", "ЗАКЛЮЧЕНИЕ" in en, f"нет 'ЗАКЛЮЧЕНИЕ' в англ (#conslusion): {en[:120]!r}")
c.check("equal", ru == en,
        f"тексты не совпали:\n  ru={ru[:120]!r}\n  en={en[:120]!r}")
c.done()
