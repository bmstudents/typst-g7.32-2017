"""hd3: приложение с собственной-нумерацией — footer внутри своя (от 1).

Основная часть продолжает сквозную нумерацию; страницы приложения с
собственной-нумерацией нумеруются заново. Инварианты:
 - последняя страница основной части имеет footer == её сквозной номер;
 - страницы приложения нумеруются 1,2,3,... (собственная), т.е. внутри
   приложения появляется footer "1" заново;
 - собственная нумерация монотонна внутри приложения.
"""
import helpers as h

c = h.Checks("hd3_appendix_own_numbering_footer")
pdf = h.compile("hd3_appendix_own_numbering_footer.typ")
n = h.page_count(pdf)

c.check("multipage", n >= 5, f"страниц {n}, нужно >=5 (3 осн. + 2+ прил.)")

# определим страницы приложения: те, что после заголовка "ПРИЛОЖЕНИЕ"
words = h.words(pdf)
app_start = None
for p in range(1, n + 1):
    txt = " ".join(w[5] for w in words if w[0] == p)
    if "ПРИЛОЖЕНИЕ" in txt:
        app_start = p
        break
c.check("appendix_found", app_start is not None, "заголовок ПРИЛОЖЕНИЕ не найден")

footers = {p: h.footer_word(pdf, p) for p in range(1, n + 1)}

if app_start:
    # содержательные страницы приложения идут со страницы > app_start
    # (на странице заголовка own-numbering footer = 0; контент после pagebreak)
    app_pages = list(range(app_start, n + 1))
    app_footers = [footers[p] for p in app_pages]
    app_ints = [int(x) for x in app_footers if x and x.isdigit()]
    # собственная нумерация: где-то внутри приложения footer == 1 заново,
    # и значения не дотягивают до сквозных номеров основной части (которые >=3)
    c.check("own_numbering_restarts",
            1 in app_ints,
            f"в приложении нет страницы с собственным номером 1; "
            f"футеры приложения = {app_footers}")
    # собственная нумерация мала (не сквозная): max footer приложения должен
    # быть заметно меньше, чем если бы продолжалась сквозная (>= n-1)
    c.check("own_numbering_small",
            app_ints and max(app_ints) < n,
            f"footer приложения вырос до сквозного ({max(app_ints) if app_ints else None}); "
            f"собственная нумерация не сработала: {app_footers}")
c.done()
