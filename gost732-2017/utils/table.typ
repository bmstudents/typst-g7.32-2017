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
