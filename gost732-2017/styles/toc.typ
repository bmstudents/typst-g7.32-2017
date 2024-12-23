#import "../g7.32-2017.config.typ": config
#import "../internal-utils/utils.typ": to_str, should_be_unnumbered_heading, should_be_ignored_heading

#let style_toc(content) = {
    let make_view(entry) = {
        let toc = none
        let disable_numbering = none
        let force_numbering = none
        let (n, ..body) = to_str(entry.body).split(" ")
        body = body.join(" ")

        // [#type(element.numbering)]
        let numbering = entry.element.numbering
        if type(numbering) == function {
            if type(numbering("1")) == dictionary {
                let dict = numbering("1")
                toc = dict.at("toc", default: none)
                disable_numbering = dict.at("disable_numbering", default: none)
                force_numbering = dict.at("force_numbering", default: none)
            }
        }

        if toc != none {
            body = toc
        }

        if disable_numbering != none {
            return [ #body ]
        } else if force_numbering != none {
            return [ #force_numbering #entry.element.body ]
        } else if should_be_unnumbered_heading(body) {
            return upper[ #body ]
        } else {
            return [ #n #body]
        }
    }

    show outline.entry.where(
        level: 1
    ): it => {
        let (element, level, body, fill, page) = it.fields()

        if should_be_ignored_heading(element) {
            return [#v(-1.5 * config.page.textSize)]
        }

        let body = make_view(it)

        [ #body #box(width: 1fr, fill) #page ]
    }

    content
}
