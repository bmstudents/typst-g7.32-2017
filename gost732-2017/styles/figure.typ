#import "../g7.32-2017.config.typ": *

#let style_figure(feature-table-small-spacing, content) = {
    let caption_style(body) = [
        #set par(justify: true, leading: 0.5em, first-line-indent: 0em)
        #box(width: 100%)[#body]
    ]

    let caption_text(caption) = [
        #caption.supplement #caption.counter.display(caption.numbering)#caption.separator #caption.body
    ]

    show figure.where(
        kind: table
    ): it => {
        set block(breakable: true)
        set figure.caption(position: top)

        let continuation = counter("continuation")

        // Верхний отступ перед таблицей задаётся weak-пробелом: на стыке
        // страниц он схлопывается, поэтому таблица, перетёкшая на новую
        // страницу, начинается ровно от верхнего поля (а не на 0.5em ниже).
        // Сам header больше не несёт верхнего inset (top: 0em).
        v(config.page.spacing, weak: true)
        table(
            stroke: 0em,
            inset: (x: 0em, top: 0em, bottom: 0.5em),
            columns: (1fr),
            table.header([#align(left)[
                #context [
                    #if continuation.get().at(0) == 0 [
                        #h(-1.25cm) #continuation.update(1) 
                        #caption_text(it.caption)
                        #v(if feature-table-small-spacing { -0.5em } else { 0em })
                    ] else [ 
                        #h(-1.25cm) Продолжение таблицы #counter(figure.where(kind: table)).display()
                        #v(if feature-table-small-spacing { -0.5em } else { 0em })
                    ]
                ]
            ]]),
            // тело прижато влево с тем же сдвигом, что и подпись (h(-1.25cm)),
            // чтобы левая граница таблицы стояла ровно под словом «Таблица»,
            // а не центрировалась по полосе
            [#h(-1.25cm)#align(left)[#it.body]]
        )
        v(-0.5em)
        v(if feature-table-small-spacing { -0.5em } else { 0em })

        context continuation.update(0)
    }

    show figure.where(
        kind: raw
    ): it => {
        set block(breakable: true)
        set figure.caption(position: top)

        let continuation = counter("continuation")

        // Верхний отступ перед таблицей задаётся weak-пробелом: на стыке
        // страниц он схлопывается, поэтому таблица, перетёкшая на новую
        // страницу, начинается ровно от верхнего поля (а не на 0.5em ниже).
        // Сам header больше не несёт верхнего inset (top: 0em).
        v(config.page.spacing, weak: true)
        table(
            stroke: 0em,
            inset: (x: 0em, top: 0em, bottom: 0.5em),
            columns: (1fr),
            table.header([#align(left)[
                #context [
                    #if continuation.get().at(0) == 0 [
                        #h(-1.25cm) #continuation.update(1) 
                        #caption_text(it.caption)
                        #v(if feature-table-small-spacing { -0.5em } else { 0em })
                    ] else [ 
                        #h(-1.25cm) Продолжение листинга #counter(figure.where(kind: raw)).display()
                        #v(if feature-table-small-spacing { -0.5em } else { 0em })
                    ]
                ]
            ]]),
            [#it.body]
        )
        v(-0.5em)
        v(if feature-table-small-spacing { -0.5em } else { 0em })

        context continuation.update(0)
    }

    show figure.caption: it => {
        caption_style(it)
    }

    show figure.where(
        kind: image
    ): it => {
        // тело и подпись рисунка — единый неразрывный блок: на стыке страниц
        // подпись «Рисунок N» не отрывается от рисунка (orphan-защита)
        block(breakable: false)[
            #it.body
            #v(if feature-table-small-spacing { -0.5em } else { 0em })
            #it.caption
        ]
    }

    set figure.caption(
        separator: [ -- ]
    )

    content
}
