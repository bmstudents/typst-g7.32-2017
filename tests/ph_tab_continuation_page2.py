"""6 tab-continuation (расположение): слово 'Продолжение' физически на странице >1
и стоит у верха этой страницы (это шапка-повтор, а не середина тела)."""
import helpers as h

c = h.Checks("ph_tab_continuation_page2")
pdf = h.compile("ph_tab_continuation_page2.typ")

cont = [w for w in h.words(pdf) if w[5] == "Продолжение"]
c.check("continuation_exists", len(cont) > 0, "слова 'Продолжение' нет в pdf")

if cont:
    page, _, _, _, _, _ = cont[0]
    c.check("on_later_page", page > 1, f"'Продолжение' на стр.{page}, ожидалось >1")
    # 'Продолжение' — самое верхнее слово своей страницы (шапка повтора).
    fw = h.first_word(pdf, page)
    c.check("near_top", fw is not None and fw[1] == "Продолжение",
            f"верхнее слово стр.{page} = '{fw[1] if fw else None}', не 'Продолжение'")
else:
    c.check("on_later_page", False, "нет слова 'Продолжение'")
    c.check("near_top", False, "нет слова 'Продолжение'")
c.done()
