"""h4_subsection_spacing_exact: флаг `фича-отступ-перед-подразделом: да`
добавляет вертикальный зазор ровно ~config.spacing (≈14.8pt) перед ВТОРЫМ
подразделом, и НЕ трогает первый подраздел (он идёт сразу после заголовка
раздела).

Идентичные документы (одни и те же подзаголовки «Алеф»/«Бейт»), отличается
только show-rule (.with(флаг) vs без). Сравниваем абсолютные yMin подзаголовков.

Жёсткость (точные числа, не «больше»):
  1) Первый подраздел: |y_on - y_off| < 1pt — флаг его не двигает.
  2) Второй подраздел: дельта (on - off) в окне 14.8 ± 3 → [11.8 .. 17.8].
     Узкое окно вокруг измеренного config.spacing≈14.84, а не «>8».
  3) Дельта второго СТРОГО больше дельты первого минимум на 11pt — отдельная
     проверка относительности (зазор появляется именно у второго).
"""
import helpers as h

c = h.Checks("h4_subsection_spacing_exact")
pdf_on = h.compile("h4_subsection_spacing_exact_on.typ")
pdf_off = h.compile("h4_subsection_spacing_exact_off.typ")

y1_on = h.y_of(pdf_on, "Алеф")
y1_off = h.y_of(pdf_off, "Алеф")
y2_on = h.y_of(pdf_on, "Бейт")
y2_off = h.y_of(pdf_off, "Бейт")

c.check("found_all",
        None not in (y1_on, y1_off, y2_on, y2_off),
        f"не нашли подзаголовки: on=({y1_on},{y2_on}) off=({y1_off},{y2_off})")

if None not in (y1_on, y1_off, y2_on, y2_off):
    d1 = y1_on - y1_off
    d2 = y2_on - y2_off

    # 1. Первый подраздел не сдвигается флагом.
    c.check("first_subsection_unchanged",
            abs(d1) < 1.0,
            f"первый подраздел сдвинулся флагом: on={y1_on:.2f} off={y1_off:.2f} "
            f"(дельта {d1:.2f}, ждём ~0)")

    # 2. Второй подраздел опускается ровно на ~config.spacing (14.8 ± 3).
    c.check("second_delta_is_spacing",
            11.8 <= d2 <= 17.8,
            f"дельта второго подраздела {d2:.2f} вне окна [11.8..17.8] "
            f"(ждём ≈14.8 = config.spacing): on={y2_on:.2f} off={y2_off:.2f}")

    # 3. Относительность: добавочный зазор именно у второго, не у первого.
    c.check("only_second_gets_gap",
            d2 - abs(d1) >= 11.0,
            f"добавочный зазор не локализован на втором: d1={d1:.2f} d2={d2:.2f} "
            f"(d2-|d1|={d2-abs(d1):.2f}, ждём >=11)")

c.done()
