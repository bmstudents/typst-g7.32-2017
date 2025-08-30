#let config = (
    figure:(
        inset: 10pt,
    ),
    raw:(
        font: "Courier New",
        size: 12pt,
    ),
    toc:(
        label: "Содержание",
        align: left
    ),
    page:(
        textSize: 14pt,
        alignNum: center,
        paper: "a4",
        margin: (left: 30mm, right: 15mm, top: 20mm, bottom: 20mm),
        font: "Times New Roman",
        parIndent: 1.25cm,
        spacing: 1em
    ),
    list: (
        indent: 1em
    ),
    heading: (
        numbering: "1.1",
        counter: counter("heading"),
        l1: (
            pagebreak: true,
            weight:"bold",
            size: 14pt,
        ),
        l2: (
            pagebreak: false,
            weight:"bold",
            size: 14pt,
            upper: false,
            align: left,
        ),
        l3: (
            pagebreak: false,
            weight:"bold",
            size: 14pt,
            upper: false,
            align: left,
        ),
        l4: (
            pagebreak: false,
            weight:"bold",
            size: 14pt,
            upper: false,
            align: left,
        ),
    )
)

#let да = true
#let нет = false
#let по-умолчанию = none
