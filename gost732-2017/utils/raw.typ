#import "../g7.32-2017.config.typ": config

#let code(data, placement: none, content) = {
    data = box(
        stroke: black, 
        inset: config.figure.inset, 
        width: 100%
    )[ 
        #set align(left)
        #set text(font: config.raw.font, size: config.raw.size)
        #data
    ]

    return figure(
        data,
        caption: content,
        gap: config.page.spacing,
        supplement: [Листинг],
        kind: raw,
        placement: placement,
    )
}

#let листинг(
    код, 
    расположение: none,
    content
) = code(код, placement: расположение, content)
