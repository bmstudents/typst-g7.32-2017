#import "../g7.32-2017.config.typ": config
#import "../utils/heading.typ": список_использованных_источников_заголовок

#let style_page(content) = {
    let page_numbering(content) = {
        set page(
            footer: [
                #set text(size: config.page.textSize)
                #set align(config.page.alignNum)
                #context counter(page).display("1")
            ]
        )
        
        content
    }
    show: page_numbering

    set page(
        paper: config.page.paper,
        margin: config.page.margin,
    )

    set text(
        font: config.page.font, 
        size: config.page.textSize, 
        lang: "ru",
        costs: (hyphenation: 1000%)
    )
    
    set align(top)

    set par(
        leading: config.page.spacing, 
        spacing: config.page.spacing, 
        first-line-indent: (amount: config.page.parIndent, all: true),
        justify: true
    )

    // Писать только номер у ссылок
    set ref(supplement: it => [])

    // https://typst.app/docs/reference/model/ref/
    show ref: it => {
        let eq = math.equation
        let el = it.element
        if el != none and el.func() == eq {
            link(el.location(),numbering(
            el.numbering,
            ..counter(eq).at(el.location())
            ))
        } else {
            it
        }
    }

    set bibliography(
        title: none,
        style: "gost-r-705-2008-numeric",
        full: true
    )

    set heading(numbering: "1")

    show bibliography: it => {
        список_использованных_источников_заголовок
        v(0.5em)

        set par(justify: true)
        it
    }

    content
}
