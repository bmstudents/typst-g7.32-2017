#import "../g7.32-2017.config.typ": config

#let style_figure(content) = {
    show figure.where(
        kind: table
    ): it => {
        set block(breakable: true)
        set figure.caption(position: top)
        show figure.caption: set align(left)

        it
    }

    show figure.where(
        kind: raw
    ): it => {
        set figure.caption(position: top)
        show figure.caption: set align(left)

        it
    }

    show figure: it => {
        show figure.caption: it => {
            set par(justify: false, leading: 0.65em)
            set text(size: config.page.textSize)
            it
        }

        it
        hide()[
            #v(-24pt)
            #par[empty]
        ]
    }

    set table(inset: config.figure.inset)

    content
}
