#import "../g7.32-2017.config.typ": config
#import "../internal-utils/utils.typ": to_str, should_be_unnumbered_heading, should_be_ignored_heading

#let style_toc(content) = {
    
    show outline.entry: it => {
        if should_be_ignored_heading(it.element) {
            return []
        }

        link(
            it.element.location(),
            [ 
                #let text = if it.element.supplement == [Раздел] {
                    it.element.body
                } else {
                    it.element.supplement
                };

                #if should_be_unnumbered_heading(it.element) {
                    it.indented(
                        none,
                        [ #upper[#text] #box(width: 1fr, it.fill) #it.page() ]
                    )
                } else {
                    it.indented(
                        [ #it.prefix() #h(-0.5em) ],
                        [ #text #box(width: 1fr, it.fill) #it.page() ]
                    )
                }
            ]
        )
    }
    
    content
}
