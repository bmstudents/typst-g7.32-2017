#import "../g7.32-2017.config.typ": config

#let table_figure(
    data,
    placement: none,
    content
) = {
    return figure(
        data,
        caption: content,
        gap: config.page.spacing,
        supplement: [Таблица],
        kind: table,
        placement: placement,
    )
}

#let таблица(
    рисунок,
    расположение: none,
    content,
) = table_figure(
    рисунок,
    placement: расположение,
    content,
)

// Содержимое ячейки таблицы по ГОСТ: 12pt, без переноса по слогам,
// не разрывается между страницами.
//   размер        — кегль (12pt — основной, 10pt — для плотных таблиц)
//   выравнивание  — none (наследуется) либо left/center/right/…
#let ячейка(content, размер: 12pt, выравнивание: none) = {
    let оформленная = text(size: размер, hyphenate: false)[#block(breakable: false)[#content]]
    if выравнивание != none {
        align(выравнивание, оформленная)
    } else {
        оформленная
    }
}
