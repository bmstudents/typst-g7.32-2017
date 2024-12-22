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

    set text(font: config.page.font, size: config.page.textSize, lang: "ru")
    
    set align(top)

    set par(
        leading: config.page.spacing, 
        spacing: config.page.spacing, 
        first-line-indent: config.page.parIndent,
        justify: true
    )

    // Писать только номер у ссылок
    set ref(supplement: it => [])

    set bibliography(
        title: none,
        style: "gost-r-705-2008-numeric",
        full: true
    )

    set heading(numbering: "1")

    show bibliography: it => {
        список_использованных_источников_заголовок
        set par(justify: true)
        it
    }

    content
}
