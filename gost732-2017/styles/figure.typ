#import "../g7.32-2017.config.typ": config

#let style_figure(content) = {
    show figure.where(
        kind: table
    ): it => {
        // set par(justify: false)
        set figure.caption(position: top)
        show figure.caption: set align(left)

        it
    }

    show figure.where(
        kind: raw
    ): it => {
        set par(justify: false)
        set figure.caption(position: top)
        show figure.caption: set align(left)

        it
    }

    show figure: it => {
        it
        hide()[
            #par[empty]
        ]
    }

    set table(inset: config.figure.inset)

    content
}
