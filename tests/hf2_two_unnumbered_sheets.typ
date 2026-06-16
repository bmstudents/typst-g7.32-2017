#import "../gost732-2017/g7.32-2017.typ": *
#import "../gost732-2017/utils/insert.typ": insert-sheet
#show: гост732-2017

// Типовой диплом: титул + задание, оба вне сквозной нумерации.
#insert-sheet([ТИТУЛ], скрыть-номер: true, в-нумерации: false)
#insert-sheet([ЗАДАНИЕ], скрыть-номер: true, в-нумерации: false)

Реферат — первая нумеруемая страница.

#pagebreak()

Содержание.

#pagebreak()

Введение.
