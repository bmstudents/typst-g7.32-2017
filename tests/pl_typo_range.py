"""pl point 13: числовой диапазон '45-50' не разрывается — целиком на одной
строке в узком box 36pt. Проверяем, что '45-50' пришёл одним токеном (не
распался на '45-' / '50'), а предшествующее 'яяя' перенеслось на строку выше."""
import helpers as h

c = h.Checks("pl_typo_range")
pdf = h.compile("pl_typo_range.typ")
ws = [w for w in h.words(pdf) if not (w[5].isdigit() and w[2] > 700)]

диап = next((w for w in ws if w[5] == "45-50"), None)
яяя = next((w for w in ws if w[5] == "яяя"), None)

c.check("range_intact", диап is not None,
        f"диапазон '45-50' распался на токены: {[w[5] for w in ws]}")
# диапазон не разорван: нет осколков '45-' или '50' отдельно
c.check("no_fragments", not any(w[5] in ("45-", "50", "45") for w in ws),
        f"есть осколки диапазона: {[w[5] for w in ws]}")
if диап and яяя:
    c.check("range_below_word", диап[2] > яяя[2] + 1.0,
            f"перенос не сработал: yMin яяя={яяя[2]:.1f} 45-50={диап[2]:.1f}")
else:
    c.check("range_below_word", False, "нет слов для проверки")
c.done()
