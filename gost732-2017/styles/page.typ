#import "../g7.32-2017.config.typ": config

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

    set text(font: config.page.font, size: config.page.textSize, lang: "ru")
    
    set align(top)

    set par(
        leading: config.page.spacing, 
        spacing: config.page.spacing, 
        first-line-indent: config.page.parIndent,
        justify: true
    )

    set figure.caption(
        separator: [ --- ]
    )

    // set figure

    show ref: it => {
        let el = it.element
        if el != none and el.func() == figure {
            // Не писать "Рисунок", а только номер
            link(el.location(),numbering(
            el.numbering,
            ..counter(figure).at(el.location())
            ))
        } else {
            it
        }
        
    }

    content
}
