r"""h5_nested_list_indent: вложенный маркир. список — у вложенного уровня маркер «–»
имеет БОЛЬШИЙ x, чем у верхнего уровня.

Жёсткость: измеряем X-координаты маркеров-тире в координатном слое, не просто
наличие текста. Фиксируем измеримый инвариант «inner.x > outer.x» и реальное
поведение пакета (show-rule в styles/list.typ рендерит phase.body рекурсивно).

ДОКУМЕНТИРОВАННЫЙ ФАКТ ПОВЕДЕНИЯ: пакетный show list (styles/list.typ) для каждого
phase печатает `#h(parIndent) -- #phase.body \`. Когда phase.body сам является
списком, вложенный список разворачивается ВНУТРИ строки родительского пункта —
он НЕ переносится на отдельную строку (родитель и вложенный пункт делят один
baseline). Тем не менее накопленный горизонтальный отступ даёт вложенному маркеру
строго больший x. Этот тест проверяет именно X-инвариант и фиксирует факт инлайна.
"""
import helpers as h

c = h.Checks("h5_nested_list_indent")
pdf = h.compile("h5_nested_list_indent.typ")
W = h.words(pdf)

DASH = "–"  # en-dash — маркер ГОСТ-списка
markers = [w for w in W if w[5] == DASH]

# 3 пункта (альфа, бета, гамма) → ожидаем 3 тире-маркера.
c.check("three_markers", len(markers) == 3,
        f"ожидали 3 тире-маркера (2 верх. + 1 вложенный), нашли {len(markers)}: "
        f"{[(round(m[1],1), round(m[2],1)) for m in markers]}")

# Привязываем маркеры к словам-телам, чтобы надёжно отличить уровни.
def word_after(marker):
    """Ближайшее справа на том же baseline слово-тело."""
    same_line = [w for w in W if w[0] == marker[0]
                 and abs(w[2] - marker[2]) < 3 and w[1] > marker[3] and w[5] != DASH]
    return min(same_line, key=lambda w: w[1])[5] if same_line else None

labels = {word_after(m): m for m in markers}
m_alpha = labels.get("альфа")
m_beta = labels.get("бета")
m_gamma = labels.get("гамма")

c.check("all_three_identified",
        all(m is not None for m in (m_alpha, m_beta, m_gamma)),
        f"не опознаны маркеры по телам; найдено: {sorted(k for k in labels if k)}")

if all(m is not None for m in (m_alpha, m_beta, m_gamma)):
    LEFT_MARGIN = 30 * 2.83464567       # 30mm ≈ 85.04
    PAR_INDENT = 1.25 * 28.3464567      # 1.25cm ≈ 35.43
    TOP_X = LEFT_MARGIN + PAR_INDENT    # ≈ 120.47 — уровень 1

    # Верхние уровни (альфа, гамма) — на абзацном отступе ≈ 120.47.
    c.check("top_level_at_indent",
            abs(m_alpha[1] - TOP_X) < 4 and abs(m_gamma[1] - TOP_X) < 4,
            f"x верхних маркеров: альфа={m_alpha[1]:.1f}, гамма={m_gamma[1]:.1f}; "
            f"ожидали ≈{TOP_X:.1f}")

    # ГЛАВНЫЙ ИНВАРИАНТ: вложенный маркер строго правее верхнего (больший x).
    c.check("nested_marker_x_greater",
            m_beta[1] > m_alpha[1] + 10 and m_beta[1] > m_gamma[1] + 10,
            f"вложенный маркер x={m_beta[1]:.1f} НЕ строго правее верхних "
            f"(альфа={m_alpha[1]:.1f}, гамма={m_gamma[1]:.1f}) — вложенность не отражена в отступе")

    # После перехода на нативные list/enum вложенный пункт переносится на
    # ОТДЕЛЬНУЮ строку (ниже родителя) — корректное ГОСТ-поведение, а не inline.
    c.check("nested_on_own_line",
            m_beta[2] > m_alpha[2] + 3,
            f"вложенный пункт должен быть на отдельной строке ниже родителя; "
            f"y(бета)={m_beta[2]:.1f} не ниже y(альфа)={m_alpha[2]:.1f}")

c.done()
