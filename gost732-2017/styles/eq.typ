#import "../g7.32-2017.config.typ": config

#let style_eq(content) = {
    set math.equation(numbering: "(1)")

    show math.equation.where(block: true): it => [
        #block(
            above: 2.5em,
            below: 2.5em
        )[ #it ]
        #par[
            #v(-2em)
            #hide[kostyl before typst 0.13.0]
        ]
    ]

    content
}
