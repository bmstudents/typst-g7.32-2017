#import "../g7.32-2017.config.typ":config

#let style_list(content) = {
    // Нативные list/enum вместо рукописного show-цикла: typst сам даёт
    // висячий отступ (перенос строки под текст, не под маркер), корректную
    // вложенность и учёт явных номеров (5. → 5)). Маркер «–», нумерация «N)»
    // по ГОСТ, отступ маркера = абзацный (1.25 см).
    set list(
        marker: ([–], [–], [–]),
        indent: config.page.parIndent,
        body-indent: 0.5em,
    )
    set enum(
        numbering: "1)",
        indent: config.page.parIndent,
        body-indent: 0.5em,
        full: true,
    )

    content
}
