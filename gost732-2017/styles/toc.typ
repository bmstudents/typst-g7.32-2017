#import "../g7.32-2017.config.typ": config
#import "../internal-utils/utils.typ": to_str, should_be_unnumbered_heading, should_be_upper_heading, should_be_ignored_heading

#let style_toc(content) = {
    
    show outline: it => {
        it
        context pagebreak(weak: true)
    }

    show outline.entry: it => {
        if should_be_ignored_heading(it.element) {
            return []
        }

        // link(
        //     it.element.location(),
        //     [ 
        //         #let text = if it.element.supplement == [Раздел] {
        //             it.element.body
        //         } else {
        //             it.element.supplement
        //         };

        //         #let text = if should_be_unnumbered_heading(it.element) {
        //             // it.indented(
        //             //     none,
        //             //     [ #upper[#text] #box(width: 1fr, it.fill) #it.page() ]
        //             // )
        //             // par(first-line-indent: 0cm, justify: true)[ #upper[#text] #box(width: 1fr, it.fill) #it.page() ]
        //             upper[#text]
        //         } else {
        //             // it.indented(
        //             //     [ #it.prefix() #h(-0.5em) ],
        //             //     [ #text #box(width: 1fr, it.fill) #it.page() ]
        //             // )
        //             // par(first-line-indent: 0cm, justify: true)[ #it.prefix() #text #box(width: 1fr, it.fill) #it.page() ]
        //             [ #it.prefix() #text ]
        //         }

        //         #par(first-line-indent: 0cm, justify: true)[ #text #box(width: 1fr, it.fill) #it.page() ]
        //     ]
        // )
        
        let text = if it.element.supplement == [Раздел] {
            it.element.body
        } else {
            it.element.supplement
        };

        let text = if should_be_unnumbered_heading(it.element) {
            text
        } else {
            [ #it.prefix() #text ]
        }

        let text = if should_be_upper_heading(it.element) {
            upper[ #text ]
        } else {
            text
        }


        let indent_amount = if it.level > 1 {
            1em * (it.level - 1)
        } else {
            0em
        }

        [
            #context {
                grid(
                    columns: (indent_amount, 1fr),
                    align: (left + bottom, right + bottom),
                    if it.level > 1{
                        "  "*(it.level - 1)
                    }else{
                        ""
                    },
                    box(width: 100%)[#set par(justify: true); #text #box(width: 1fr, it.fill) #it.page()],
                )
            }
        ]
    }
    
    content
}
