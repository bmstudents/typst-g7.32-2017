#let img-counter = counter("image");

#let config = (
    raw:(
        theme:"",
        bg: luma(240),
        num: false,
        size: 14pt,
        splitter: "|",
        counter: counter("listing")
    ),
    toc:(
        label: "Содержание",
        align: left
    ),
    img:(
        counter: img-counter
    ),
    table:(
        counter: counter("table")
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
            upper: true,
            align: center,
            indent: 1em
        ),
        l2: (
            pagebreak: false,
            weight:"bold",
            size: 14pt,
            upper: false,
            align: left,
            indent: 1em
        ),
        l3: (
            pagebreak: false,
            weight:"bold",
            size: 14pt,
            upper: false,
            align: left,
            indent: 1em
        ),
        l4: (
            pagebreak: false,
            weight:"bold",
            size: 14pt,
            upper: false,
            align: left,
            indent: 1em
        ),
    )
)
