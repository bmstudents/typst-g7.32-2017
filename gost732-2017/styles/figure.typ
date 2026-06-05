#import "../g7.32-2017.config.typ": config

#let style_figure(feature-table-small-spacing, content) = {
    let caption_style(body) = [
        #set par(justify: true, leading: 0.3em, first-line-indent: 0em)
        #body
    ]

    let caption_block_style(body) = box(width: 100%)[
        #set par(justify: true, leading: 0.3em, first-line-indent: 0em)
        #body
    ]

    let caption_text(caption) = [
        #caption.supplement #caption.counter.display(caption.numbering)#caption.separator #caption.body
    ]

    show figure: it => {
        show figure.caption: it => {
            caption_style(it)
        }

        it
        hide()[
            #v(-24pt)
            #par[empty]
        ]
    }

    show figure.where(
        kind: table
    ): it => {
        set block(breakable: true)
        set figure.caption(position: top)
        show figure.caption: it => caption_style(it)

        let continuation = counter("continuation")

        v(-0.5em)
        table(
            stroke: 0em,
            inset: (x: 0em, y: 0.5em),
            columns: (1fr),
            table.header([#align(left)[
                #context [
                    #if continuation.get().at(0) == 0 {[
                        #continuation.update(1) 
                        #caption_block_style(caption_text(it.caption))
                        // Костыль, чтобы сделать межстрочный интервал 1, а не 1.5 при включенной фиче
                        #if feature-table-small-spacing == true {
                            v(-0.5em)
                        }
                    ]} else {[
                        #caption_block_style[
                            Продолжение таблицы #counter(figure.where(kind: table)).display()
                        ]
                        #if feature-table-small-spacing == true {
                            v(-0.5em)
                        }
                    ]}
                ]
            ]]),
            [#it.body]
        )
        v(-0.5em)

        context continuation.update(0)
    }

    show figure.where(
        kind: raw
    ): it => {
        set block(breakable: true)
        set figure.caption(position: top)
        show figure.caption: it => caption_style(it)

        let continuation = counter("continuation")

        v(-0.5em)
        table(
            stroke: 0em,
            inset: (x: 0em, y: 0.5em),
            columns: (1fr),
            table.header([#align(left)[
                #context [
                    #if continuation.get().at(0) == 0 {[ 
                        #continuation.update(1) 
                        #caption_block_style(caption_text(it.caption))
                        #if feature-table-small-spacing == true {
                            v(-0.5em)
                        }
                    ]} else {[ 
                        #caption_block_style[
                            Продолжение листинга #counter(figure.where(kind: raw)).display()
                        ]
                        #if feature-table-small-spacing == true {
                            v(-0.5em)
                        }
                    ]}
                ]
            ]]),
            [#it.body]
        )
        v(-0.5em)

        context continuation.update(0)
    }

    set figure.caption(
        separator: [ -- ]
    )

    content
}
