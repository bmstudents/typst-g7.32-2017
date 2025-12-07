#import "../g7.32-2017.config.typ": config

#let колво-страниц = context {
    let appendix = query(<internal-appendix>)

    return counter(page).final().at(0)
}

#let колво-рисунков = context {
    let appendix = query(<internal-appendix>)

    if appendix.len() > 0 {
        return counter(figure.where(
            kind: image
        )).at(
            appendix.first().location()
        ).at(0)
    } else {
        return counter(figure.where(
            kind: image
        )).final().at(0)
    }
}

#let колво-таблиц = context {
    let appendix = query(<internal-appendix>)

    if appendix.len() > 0 {
        return counter(figure.where(
            kind: table
        )).at(
            appendix.first().location()
        ).at(0)
    } else {
        return counter(figure.where(
            kind: table
        )).final().at(0)
    }
}

#let колво-источников = context {
    // https://github.com/typst/typst/discussions/4344
    return query(selector(ref)).filter(it => it.element == none).map(it => it.target).dedup().len()
}

#let колво-приложений = context {
    return query(<internal-appendix>).len()
}
