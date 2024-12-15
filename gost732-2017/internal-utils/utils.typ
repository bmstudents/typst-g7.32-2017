// https://github.com/typst/typst/issues/2196#issuecomment-1728135476
#let to_str(content) = {
    if type(content) == str {
        content
    } else if content.has("text") {
        content.text
    } else if content.has("children") {
        content.children.map(to_str).join("")
    } else if content.has("body") {
        to_str(content.body)
    } else if content == [ ] {
        " "
    }
}

#let should_be_unnumbered_heading(heading) = {
    let heading = lower(to_str(heading))
    let match_res = heading.match(regex(
        "(список испольнителей)|реферат|содержание|(термины и определения)|(определения, обозначения и сокращения)|(перечень сокращений и обозначений)|введение|заключение|(список использованных источников)|(приложение [а-яё])"
    ))

    return match_res != none and match_res.start == 0 and match_res.end == heading.len()
}
