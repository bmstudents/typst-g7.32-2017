"""pa_flag-small-spacing: фича-маленький-отступ-вокруг-таблиц да vs нет —
вертикальные интервалы вокруг таблицы различаются. С флагом 'да' пакет
вставляет дополнительные v(-0.5em) вокруг подписи и тела таблицы, поэтому
текст ПОСЛЕ таблицы и сама подпись сидят выше, чем без флага.

Сравниваем y маркерного слова, идущего сразу после таблицы, в двух компиляциях."""
import helpers as h

c = h.Checks("pa_small_spacing_body")
pdf_on = h.compile("pa_small_spacing_on.typ")
pdf_off = h.compile("pa_small_spacing_off.typ")

y_on = h.y_of(pdf_on, "ЯкорьПослеТаблицы")
y_off = h.y_of(pdf_off, "ЯкорьПослеТаблицы")

c.check("anchor_found", y_on is not None and y_off is not None,
        f"маркер не найден: on={y_on} off={y_off}")

# С флагом 'да' интервалы плотнее → маркер сидит ВЫШЕ (меньший y).
c.check("on_tighter_than_off", y_on is not None and y_off is not None and y_on < y_off,
        f"с 'да' маркер не выше: on={y_on} off={y_off} (ждём on<off)")

# Различие заметное (минимум ~0.5em ≈ 7pt из-за двух v(-0.5em)).
c.check("delta_significant",
        y_on is not None and y_off is not None and (y_off - y_on) > 5.0,
        f"разница интервалов мала: off-on={None if y_on is None else y_off - y_on} (ждём >5)")
c.done()
