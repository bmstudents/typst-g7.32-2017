"""pa_flag-hyphenate-off (аспект 2): прямое сравнение нет vs да на одном слове
в узком box. С 'нет' слово в одну строку; с 'да' оно разбито на несколько
фрагментов — число строк тела с буквами строго больше."""
import helpers as h

c = h.Checks("pa_hyphenate_off_vs_on")
pdf_off = h.compile("pa_hyphenate_off.typ")
pdf_on = h.compile("pa_hyphenate_on.typ")


def body_lines(pdf):
    return [l.strip() for l in h.text(pdf).splitlines()
            if l.strip() and not l.strip().isdigit()]


off = body_lines(pdf_off)
on = body_lines(pdf_on)

c.check("off_single_line", len(off) == 1,
        f"с 'нет' слово не на одной строке: {off!r}")
c.check("on_multiple_lines", len(on) > 1,
        f"с 'да' слово не разбито на строки: {on!r}")
c.check("on_more_lines_than_off", len(on) > len(off),
        f"перенос не увеличил число строк: off={len(off)} on={len(on)}")
c.done()
