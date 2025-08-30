#import "../g7.32-2017.config.typ": config
#import "../internal-utils/utils.typ": to_str, should_be_unnumbered_heading, is_appendix

#let style_heading(content) = {

    set heading(numbering: config.heading.numbering, supplement: auto)

    // https://discord.com/channels/1054443721975922748/1088371919725793360/1367845473183993928
    show heading.where(): set block(below: 3em) // Расстояние между заголовком и текстом
    show heading.where(): it => {
        v(1em, weak: true) // Расстояние между заголовками

        it
    }

    show heading.where(level: 1): it => {
        set text(config.heading.l1.size, weight: config.heading.l1.weight, hyphenate: false)

        if it.outlined and config.heading.l1.pagebreak {
            colbreak(weak: true)
        }

        if it.numbering == none {
            context counter(heading).update(0)
        }

        if should_be_unnumbered_heading(it) {
            context counter(heading).update(0)
            it = block[#it.body]
        }
    
        upper[#align(center)[
            #it
        ]]

    }

    show heading.where(level: 2): it => {
        set text(config.heading.l2.size, weight: config.heading.l2.weight, hyphenate: false)

        if config.heading.l2.pagebreak {
            colbreak(weak: true)
        }

        if config.heading.l2.upper {
            it = upper(it)
        }

        align(config.heading.l2.align)[
            #it
        ]
    }

    show heading.where(level: 3): it => {
        set text(config.heading.l3.size, weight: config.heading.l3.weight, hyphenate: false)

        if config.heading.l3.pagebreak {
            colbreak(weak: true)
        }

        if config.heading.l3.upper {
            it = upper(it)
        }

        align(config.heading.l3.align)[
            #it
        ]
    }

    show heading.where(level: 4): it => {
        set text(config.heading.l4.size, weight: config.heading.l4.weight, hyphenate: false)

        if config.heading.l4.pagebreak {
            colbreak(weak: true)
        }

        if config.heading.l4.upper {
            it = upper(it)
        }

        align(config.heading.l4.align)[
            #it
        ]
    }

    content
}
