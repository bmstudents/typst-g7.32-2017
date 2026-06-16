"""pa_flag-subheading-on (аспект 2): с флагом 'да' вертикальный зазор между
концом первого подраздела и заголовком второго подраздела БОЛЬШЕ, чем без
флага — на величину вставленной пустой строки. Меряем зазор между 'первого'
(последнее слово тела первого подраздела) и 'ПодразделБета'."""
import helpers as h

c = h.Checks("pa_subheading_gap")
pdf_on = h.compile("pa_subheading_on.typ")
pdf_off = h.compile("pa_subheading_off.typ")


def gap(pdf):
    y_body = h.y_of(pdf, "первого")        # «...первого подраздела.»
    y_head = h.y_of(pdf, "ПодразделБета")
    return None if (y_body is None or y_head is None) else y_head - y_body


g_on = gap(pdf_on)
g_off = gap(pdf_off)

c.check("found_all", g_on is not None and g_off is not None,
        f"якоря не найдены: on={g_on} off={g_off}")
c.check("gap_larger_with_flag",
        g_on is not None and g_off is not None and (g_on - g_off) > 8.0,
        f"зазор не вырос: on={g_on} off={g_off} (ждём on-off>8)")
c.done()
