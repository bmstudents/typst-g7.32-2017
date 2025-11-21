#import "../g7.32-2017.config.typ": config
#import "../internal-utils/utils.typ": to_str, should_be_unnumbered_heading, is_appendix

#let style_heading(content) = {

    set heading(numbering: config.heading.numbering, supplement: auto)
    show heading: set block(sticky: true)

    show heading: it => {
        par[ #counter(heading).display() #it.body ]
    }

    show heading.where(level: 1): it => {
        set text(config.heading.l1.size, weight: config.heading.l1.weight, hyphenate: false)

        if it.outlined and config.heading.l1.pagebreak {
            pagebreak(weak: true)
        }

        if it.numbering == none or should_be_unnumbered_heading(it) {
            context counter(heading).update(0)
            align(center)[#upper[
                #it.body
            ]]
        } else {
            align(left)[
                #it
            ]
        }
    }

    show heading.where(level: 2): it => {
        set text(config.heading.l2.size, weight: config.heading.l2.weight, hyphenate: false)

        if config.heading.l2.pagebreak {
            pagebreak(weak: true)
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
            pagebreak(weak: true)
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
            pagebreak(weak: true)
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
