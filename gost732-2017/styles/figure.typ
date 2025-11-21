#import "../g7.32-2017.config.typ": config

#let style_figure(content) = {
    show figure.where(
        kind: table
    ): it => {
        set block(breakable: true)
        set figure.caption(position: top)
        show figure.caption: set align(left)

        let continuation = counter("continuation")

        v(-0.5em)
        table(
            stroke: 0em,
            inset: (x: 0em, y: 0.5em),
            columns: (1fr),
            table.header([#align(left)[
                #context [ 
                    #let table-small-offset = query(selector(
                        <gost732-2017-feature-table-head-small-spacing>
                    ).before(here())).last().value
                    #if continuation.get().at(0) == 0 {[
                        #continuation.update(1) 
                        #it.caption
                        // Костыль, чтобы сделать межстрочный интервал 1, а не 1.5 при включенной фиче
                        #if table-small-offset == true {
                            v(-0.5em)
                        }
                    ]} else {[
                        #set par(justify: true, leading: 0.65em, first-line-indent: 0cm)
                        #set text(size: config.page.textSize)
                        Продолжение таблицы #counter(figure.where(kind: table)).display()
                        #if table-small-offset == true {
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
        show figure.caption: set align(left)

        let continuation = counter("continuation")

        v(-0.5em)
        table(
            stroke: 0em,
            inset: (x: 0em, y: 0.5em),
            columns: (1fr),
            table.header([#align(left)[
                #context [
                    #let table-small-offset = query(selector(
                        <gost732-2017-feature-table-head-small-spacing>
                    ).before(here())).last().value
                    #if continuation.get().at(0) == 0 {[ 
                        #continuation.update(1) 
                        #it.caption
                        #if table-small-offset == true {
                            v(-0.5em)
                        }
                    ]} else {[ 
                        #set par(justify: true, leading: 0.65em, first-line-indent: 0cm)
                        #set text(size: config.page.textSize)
                        Продолжение листинга #counter(figure.where(kind: raw)).display()
                        #if table-small-offset == true {
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

    show figure: it => {
        show figure.caption: it => {
            set par(justify: true, leading: 0.65em)
            set text(size: config.page.textSize)
            it
        }

        it
        hide()[
            #v(-24pt)
            #par[empty]
        ]
    }

    set figure.caption(
        separator: [ --- ]
    )

    content
}
