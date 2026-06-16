"""pj 11: счётчик рисунков в приложении сбрасывается -> первый рис 'А.1'."""
import helpers as h

c = h.Checks("pj_app_figure_numbering_reset")
pdf = h.compile("pj_app_figure_numbering_reset.typ")
t = " ".join(h.text(pdf).split())

# Основной документ дал 'Рисунок 1' и 'Рисунок 2'.
c.check("main_fig1", "Рисунок 1" in t, f"нет 'Рисунок 1' (основной док) в:\n{t[:400]}")
c.check("main_fig2", "Рисунок 2" in t, f"нет 'Рисунок 2' (основной док) в:\n{t[:400]}")

# Первый рисунок приложения сброшен на .1, а не продолжил с .3.
c.check("appendix_fig_reset", "Рисунок А.1" in t,
        f"счётчик рисунков в приложении не сброшен на 'А.1':\n{t[:400]}")
c.check("no_continued", "Рисунок А.3" not in t,
        f"счётчик не сброшен (есть 'А.3'):\n{t[:400]}")
c.done()
