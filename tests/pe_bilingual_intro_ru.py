"""pe_bilingual_intro_ru: рус #введение и англ #introduction дают одинаковый текст заголовка.

Компилируем обе версии и сравниваем нормализованный текстовый слой целиком —
алиасы обязаны быть идентичны (introduction === введение в пакете).
"""
import helpers as h

c = h.Checks("pe_bilingual_intro_ru")
ru = " ".join(h.text(h.compile("pe_bilingual_intro_ru.typ")).split())
en = " ".join(h.text(h.compile("pe_bilingual_intro_en.typ")).split())

c.check("ru_has_heading", "ВВЕДЕНИЕ" in ru, f"нет 'ВВЕДЕНИЕ' в рус: {ru[:120]!r}")
c.check("en_has_heading", "ВВЕДЕНИЕ" in en, f"нет 'ВВЕДЕНИЕ' в англ: {en[:120]!r}")
c.check("equal", ru == en,
        f"тексты не совпали:\n  ru={ru[:120]!r}\n  en={en[:120]!r}")
c.done()
