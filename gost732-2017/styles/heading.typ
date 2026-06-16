#import "../g7.32-2017.config.typ": config
#import "../internal-utils/utils.typ": to_str, should_be_unnumbered_heading, is_appendix

#let style_heading(feature-space-before-subheading, content) = {
    set heading(numbering: config.heading.numbering, supplement: auto)

    let sticky_heading(body) = block(
        sticky: true,
        width: 100%,
        spacing: 1em,
    )[#body]

    show heading: it => {
        sticky_heading[#par(
            leading: config.page.spacing, 
            spacing: config.page.spacing,
            first-line-indent: (amount: config.page.parIndent, all: true),
            justify: false
        )[
            #counter(heading).display() #it.body
        ]]
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

        // Перед подразделом (1.2, 3.3 …) ставится одна пустая строка,
        // КРОМЕ первого подраздела сразу после заголовка раздела (2 — 2.1).
        // Считаем подразделы 2-го уровня после последнего заголовка
        // раздела: если они уже были — текущий не первый, нужен отступ.
        if feature-space-before-subheading {
            context {
                // before(here()) включает сам текущий заголовок последним
                // элементом (inclusive: false в typst 0.14.2 его не убирает),
                // поэтому отбрасываем последний.
                let before = query(selector(heading).before(here()))
                let before = if before.len() > 0 { before.slice(0, before.len() - 1) } else { before }
                let lvl1 = before.enumerate().filter(p => p.at(1).level == 1)
                let start = if lvl1.len() > 0 { lvl1.last().at(0) + 1 } else { 0 }
                let subs-before = before.slice(start).filter(h => h.level == 2)
                if subs-before.len() > 0 {
                    v(config.page.spacing, weak: false)
                }
            }
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
