#import "../g7.32-2017.config.typ": config

#let style_raw(content) = {
    show raw: it => {
        box(
            fill: config.raw.bg,
            inset: (x:6pt, y:0pt),
            outset: (y:3pt),
            radius: 4pt,
            align(left)[#it]
        )
    }
    
    content
}
