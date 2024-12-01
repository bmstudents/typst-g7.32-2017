#import "../g7.32-2017.config.typ": config

#let img(
    image,
    placement,
    content
) = {
    return figure(
        image,
        caption: content,
        gap: config.page.spacing,
        supplement: [Рисунок],
        kind: "рисунок",
        placement: placement
    )
}

#let рис(
    рисунок,
    placement: auto,
    content,
) = img(рисунок, placement, content)

#let размер(количество-строчек) = {
    return 14pt * количество-строчек - 3pt
}
