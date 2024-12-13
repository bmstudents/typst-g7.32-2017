#import "../g7.32-2017.config.typ": config

#let img(
    data,
    placement: none,
    content
) = {
    // content += [ #v(14pt) ]
    return figure(
        data,
        caption: content,
        gap: config.page.spacing,
        supplement: [Рисунок],
        kind: image,
        placement: placement
    )
}

#let рис(
    рисунок,
    расположение: none,
    content,
) = img(рисунок, placement: расположение, content)

#let размер(количество-строчек) = {
    return 14pt * количество-строчек - 3pt
}
