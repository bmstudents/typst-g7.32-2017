#import "../g7.32-2017.config.typ": config

#let img(
    data,
    placement: none,
    повернуто: false,
    content
) = {
    // повернуто: альбомная иллюстрация (широкая схема, А1-плакат) —
    // тело поворачивается на 90°, подпись «Рисунок N» остаётся горизонтальной
    return figure(
        if повернуто { rotate(-90deg, reflow: true, data) } else { data },
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
    повернуто: false,
    content,
) = img(рисунок, placement: расположение, повернуто: повернуто, content)

#let размер(количество-строчек) = {
    return 14pt * количество-строчек - 3pt
}
