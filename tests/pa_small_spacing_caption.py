"""pa_flag-small-spacing (аспект 2): различие интервалов проявляется и на
вертикальном зазоре между подписью таблицы и её первой строкой тела.
С флагом 'да' добавляется v(-0.5em) после подписи → строка тела ближе к подписи."""
import helpers as h

c = h.Checks("pa_small_spacing_caption")
pdf_on = h.compile("pa_small_spacing_on.typ")
pdf_off = h.compile("pa_small_spacing_off.typ")

# 'Таблица' — слово подписи; 'Колонка' — первая строка тела таблицы.
def gap(pdf):
    y_cap = h.y_of(pdf, "Таблица")
    y_body = h.y_of(pdf, "Колонка")
    return (y_cap, y_body, None if (y_cap is None or y_body is None) else y_body - y_cap)

cap_on, body_on, gap_on = gap(pdf_on)
cap_off, body_off, gap_off = gap(pdf_off)

c.check("found_all", None not in (gap_on, gap_off),
        f"подпись/тело не найдены: on={gap_on} off={gap_off}")

# С флагом 'да' зазор подпись→тело меньше (плотнее).
c.check("caption_gap_tighter_on",
        gap_on is not None and gap_off is not None and gap_on < gap_off,
        f"зазор не уменьшился: on={gap_on} off={gap_off} (ждём on<off)")
c.done()
