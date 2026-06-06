#import "../g7.32-2017.config.typ": config
#import "../utils/heading.typ": список_использованных_источников_заголовок
#import "../internal-utils/utils.typ": to_str, should_be_unnumbered_heading, is_appendix

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
        let el = it.element

        if el != none and el.func() == math.equation {
            return link(
                el.location(),
                numbering(el.numbering, ..counter(math.equation).at(el.location()))
            )
        }

        if el != none and el.func() == figure {
            let target = query(it.target).first()
            return numbering("1", ..counter(figure.where(kind: target.kind)).at(target.location()))
        }

        return it
    }

    set bibliography(
        title: none,
        style: "gost-r-705-2008-numeric",
        full: true
    )

    set heading(numbering: "1")

    show bibliography: it => [
        #align(center)[#список_использованных_источников_заголовок]

        #set par(justify: true)
        #it
    ]

    content
}
