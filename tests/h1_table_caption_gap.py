"""h1 ТАБЛИЦЫ #7 — ВЕРТИКАЛЬНЫЙ ЗАЗОР ПОДПИСЬ↔ТЕЛО + СОВПАДЕНИЕ ЛЕВОГО КРАЯ.

Подпись «Таблица N – …» стоит СВЕРХУ (position: top). Два инварианта:
  A) НЕТ вертикального наезда: yMin верхней строки тела > yMax подписи
     (зазор строго положительный) — текст шапки не печатается поверх подписи.
  B) ЛЕВЫЙ КРАЙ подписи и тела совпадает (по ГОСТ — общая левая граница).
     Сравниваем x0 слова «Таблица» и min(x0) верхней строки тела (±5pt).

ОЖИДАЕМЫЙ РЕЗУЛЬТАТ: (A) зазор положительный (PASS), но (B) левый край
расходится — подпись x0≈85, шапка тела «Шапка» x0≈264 (FAIL, известный баг
центрирования тела). Тест разделяет два аспекта, чтобы баг был локализован.
"""
import helpers as h

c = h.Checks("h1_table_caption_gap")
pdf = h.compile("h1_table_caption_gap.typ")
ws = [w for w in h.words(pdf) if w[0] == 1]

cap = [w for w in ws if w[5] in ("Таблица", "Заголовок", "таблицы")]
header = [w for w in ws if w[5] in ("Шапка", "Колонка")]

c.check("caption_present", any(w[5] == "Таблица" for w in cap),
        f"подпись «Таблица» не найдена: {[w[5] for w in ws]}")
c.check("body_header_present", len(header) == 2,
        f"верхняя строка тела «Шапка/Колонка» не найдена: {[w[5] for w in ws]}")

if cap and header:
    cap_ymax = max(w[4] for w in cap)
    body_ymin = min(w[2] for w in header)
    gap = body_ymin - cap_ymax

    # A) положительный зазор — нет наезда.
    c.check(
        "no_vertical_overlap",
        gap > 0,
        f"вертикальный наезд: yMax подписи={cap_ymax:.2f} >= yMin тела={body_ymin:.2f} "
        f"(зазор {gap:+.2f}pt). Подпись и шапка перекрываются.",
    )
    # зазор разумный (не схлопнут в 0 и не разорван на пол-страницы).
    c.check(
        "gap_reasonable",
        0 < gap < 60,
        f"зазор подпись↔тело {gap:.2f}pt вне (0;60) — либо наезд, либо разрыв.",
    )

    # B) совпадение левого края.
    cap_x0 = min(w[1] for w in cap if w[5] == "Таблица")
    body_x0 = min(w[1] for w in header)
    INSET = 10.0
    same = abs(body_x0 - cap_x0) <= 5 or abs((body_x0 - INSET) - cap_x0) <= 5
    c.check(
        "left_edges_aligned",
        same,
        f"левый край подписи и тела расходятся: подпись x0={cap_x0:.2f}, "
        f"шапка тела min x0={body_x0:.2f} (Δтекст={body_x0 - cap_x0:+.2f}, "
        f"Δграница={body_x0 - INSET - cap_x0:+.2f}); оба вне ±5pt. "
        f"Тело центрировано. Файл: gost732-2017/styles/figure.typ.",
    )

c.done()
