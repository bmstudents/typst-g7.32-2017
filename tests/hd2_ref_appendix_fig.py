"""hd2: @ref на рисунок В ПРИЛОЖЕНИИ должен печатать номер с буквой ('А.1').

В приложении figure-numbering переопределяется на appendix_num -> 'А.N'.
Подпись самого рисунка в приложении выводится как 'А.1'. Ссылка @ref
обязана вести на тот же номер, что и в подписи (то есть 'А.1').

Инвариант: ссылка на рисунок приложения == номер из его подписи, с буквой.
Баг-подозрение: styles/page.typ show ref хардкодит numbering("1", ...),
игнорируя figure.numbering, поэтому печатает '1' вместо 'А.1'.
"""
import re
import helpers as h

c = h.Checks("hd2_ref_appendix_fig")
pdf = h.compile("hd2_ref_appendix_fig.typ")
t = " ".join(h.text(pdf).split())

# Ссылка на основной рисунок = '1'
m_main = re.search(r"осномаркердо\s+(.+?)\s+осномаркерпосле", t)
main_ref = m_main.group(1) if m_main else "<нет>"
c.check("main_fig_ref_is_1", main_ref == "1",
        f"ссылка на основной рисунок = '{main_ref}', ожидалось '1'")

# Подпись рисунка приложения должна содержать 'А.1' (с буквой)
caption_has_a1 = re.search(r"Рисунок\s+А\.\s*1", t) is not None
c.check("appendix_caption_has_letter", caption_has_a1,
        f"в тексте нет подписи 'Рисунок А.1'; текст: {t[:400]}")

# Ссылка на рисунок приложения = 'А.1' (должна совпадать с подписью)
m_app = re.search(r"прилмаркердо\s+(.+?)\s+прилмаркерпосле", t)
app_ref = m_app.group(1) if m_app else "<нет>"
c.check("appendix_fig_ref_has_letter", app_ref == "А.1",
        f"ссылка на рисунок приложения = '{app_ref}', ожидалось 'А.1' "
        f"(хардкод numbering('1') в styles/page.typ игнорирует figure.numbering)")

c.done()
