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
    #v(1em)
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

#let unnumbered_heading(toc: none, numbering: none, content) = {
    let sup = content;
    if type(toc) == type([]) {
        sup = toc;
    }
    if type(numbering) == int or type(numbering) == str {
        numbering = (..n) => str(numbering);
    }
    heading(
        level: 1, 
        numbering: numbering,
        outlined: toc != false,
        supplement: sup
    )[
        #content
    ]
}
#let ненумерованный_заголовок(содержание: по-умолчанию, номер: по-умолчанию, content) = unnumbered_heading(toc: содержание, numbering: номер, content)
