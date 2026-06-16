"""hd3: приложение с (собственная-нумерация: нет) продолжает сквозную нумерацию.

Основная часть 1..3, затем приложение. Футеры страниц приложения должны
ПРОДОЛЖАТЬ сквозной счёт (>=4), а не перезапускаться с 1. Глобально вся
последовательность футеров должна быть монотонной 1,2,3,4,5,...
"""
import helpers as h

c = h.Checks("hd3_appendix_no_own_numbering")
pdf = h.compile("hd3_appendix_no_own_numbering.typ")
n = h.page_count(pdf)

c.check("multipage", n >= 4, f"страниц {n}, нужно >=4")

footers = [h.footer_word(pdf, p) for p in range(1, n + 1)]
ints = [int(x) for x in footers if x and x.isdigit()]

# сквозная нумерация: вся последовательность монотонна и без перезапуска на 1
restarts = sum(1 for v in ints[1:] if v == 1)
c.check("no_restart_to_1", restarts == 0,
        f"footer перезапустился на 1 при собственная-нумерация=нет: {footers}")

c.check("global_monotonic", ints == sorted(ints),
        f"сквозная нумерация не монотонна: {footers}")

# финальный номер должен достигать числа страниц (сквозная до конца)
c.check("reaches_last_page", ints and max(ints) == n,
        f"сквозной номер не дошёл до последней страницы: max={max(ints) if ints else None}, n={n}, {footers}")
c.done()
