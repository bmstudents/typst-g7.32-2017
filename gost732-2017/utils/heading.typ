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

#let appendix(n: (), number: ()) = {
    if n != () { number = n }
    if number == () { number = "" }
    [= Приложение #number] // TODO: автоматические номера приложений
}
#let приложение(б: (), буква: ()) = appendix(n: б, number: буква)

#let unnumbered_heading(content) = {
    // Грязный хак для прокидывания информации в функцию стиля
    let disable_numbering(.., _) = ("disable_numbering": ())

    heading(
        level: 1, 
        numbering: disable_numbering
    )[
        #content
    ]
}
#let ненумерованный_заголовок(content) = unnumbered_heading(content)

#let numbered_heading(number: (), content) = {
    // Грязный хак для прокидывания информации в функцию стиля
    let force_numbering(.., _) = ("force_numbering": number)

    heading(
        level: 1,
        numbering: force_numbering,
    )[
        #content
    ]
}
#let нумерованный_заголовок(номер: (), content) = numbered_heading(number: номер, content)
