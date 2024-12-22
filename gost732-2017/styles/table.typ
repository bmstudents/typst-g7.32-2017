#import "../g7.32-2017.config.typ": config

#let style_table(content) = {
    show figure.where(
        kind: table
    ): it => {
        set block(breakable: true)
        set figure.caption(position: top)
        show figure.caption: set align(left)

        it
    }

    set table.cell(breakable: true)

    set table(inset: config.figure.inset)

    content
}
