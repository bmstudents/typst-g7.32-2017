#import "../g7.32-2017.config.typ": config

#let style_eq(content) = {
    set math.equation(
        numbering: "(1)",
        number-align: bottom
    )

    show math.equation.where(block: true): it => [
        #block(
            above: 2.5em,
            below: 1em
        )[ #it ]
        #par[
            #hide[kostyl before typst 0.13.0]
        ]
    ]

    content
}
