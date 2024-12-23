#import "../g7.32-2017.config.typ": config

#let style_raw(content) = {
    show raw: it => {
        set align(left)
        set text(font: config.raw.font, size: config.raw.size)
        set par(leading: 0.65em, justify: false)
        set block(breakable: true)

        table(
            columns: (1fr),
            [#it]
        )
    }

    content
}
