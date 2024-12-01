#import "../g7.32-2017.config.typ": config
#import "../internal-utils/utils.typ": to_str, should_be_unnumbered_heading

#let style_toc(content) = {
    let should_be_ignored_heading(heading) = {
        let heading = lower(to_str(heading))
        let match_res = heading.match(regex(
            "реферат|содержание"
        ))

        return match_res != none and match_res.start == 0 and match_res.end == heading.len()
    }

    show outline.entry.where(
        level: 1
    ): it => {
        if should_be_ignored_heading(it.element) {
            return []
        }

        let (element, level, body, fill, page) = it.fields()

        let (n, ..body) = to_str(body).split(" ")
        body = body.join(" ")
        if not should_be_unnumbered_heading(body) {
            body = [#n #body]
        } else {
            body = upper()[ #body ]
        }

        [ #body #box(width: 1fr, fill) #page ]
    }

    content
}
