#import "../g7.32-2017.config.typ": config, по-умолчанию

#let authors_list = [
    = Список исполнителей
]
#let список_исполнителей = authors_list

#let abstract = [
    = Реферат
]
#let реферат = abstract

// Имя изменено, чтобы различать заголовок и структурный элемент
#let toc_heading = [
    = Содержание
]
#let содержание_заголовок = toc_heading

#let terms_and_definitions = [
    = Термины и определения
]
#let термины_и_определения = terms_and_definitions

#let abbreviations_and_designations = [
    = Перечень сокращений и ссылок
]
#let перечень_сокращений_и_ссылок = abbreviations_and_designations

#let terms_abbreviations_designations(content) = [
    = Определения, обозначения и сокращения
    #set par(first-line-indent: 0em)
    #content
]
#let определения_обозначения_сокращения = terms_abbreviations_designations

#let introduction = [
    = Введение
]   
#let введение = introduction

#let conslusion = [
    = Заключение
]
#let заключение = conslusion

#let bibliography_heading = [
    = СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ
]
#let список_использованных_источников_заголовок = bibliography_heading

#let unnumbered_heading(toc: none, content) = {
    // Грязный хак для прокидывания информации в функцию стиля
    let disable_numbering(.., _) = ("disable_numbering": (), "toc": toc)

    heading(
        level: 1, 
        numbering: disable_numbering,
        outlined: toc != false
    )[
        #content
    ]
}
#let ненумерованный_заголовок(содержание: по-умолчанию, content) = unnumbered_heading(toc: содержание, content)

#let numbered_heading(number: (),  toc: none, content) = {
    // Грязный хак для прокидывания информации в функцию стиля
    let force_numbering(.., _) = ("force_numbering": number, "toc": toc)

    heading(
        level: 1,
        numbering: force_numbering,
        outlined: toc != false
    )[
        #content
    ]
}
#let нумерованный_заголовок(номер: (), содержание: по-умолчанию, content) = numbered_heading(number: номер, toc: содержание, content)


#let appendix(l: none, toc: none, letter: none, content) = {
    if l != none { letter = l }
    if letter == none { letter = "" }

    ненумерованный_заголовок(содержание: toc)[= Приложение #letter] // TODO: автоматические номера приложений

    set heading(outlined: false)

    let appendix_num(.., n) = [#letter.#n]

    set figure(numbering: appendix_num)

    context counter(figure.where(kind: table)).update(0)
    context counter(figure.where(kind: raw)).update(0)
    context counter(figure.where(kind: image)).update(0)

    content
}
#let приложение(б: none, содержание: по-умолчанию, буква: none, content) = appendix(l: б, toc: содержание, letter: буква, content)
