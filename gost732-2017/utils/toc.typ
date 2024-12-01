// Составляет содержание работы.
#import "../g7.32-2017.config.typ":config

#let table_of_contents() = {
    [
        #set align(config.toc.align)
        #outline(
            indent: auto,
        )
    ]
}

#let содержание() = table_of_contents()
