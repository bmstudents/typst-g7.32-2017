// Составляет содержание работы.
#import "../g7.32-2017.config.typ": config
#import "./heading.typ": содержание_заголовок

#let table_of_contents() = {
    [
        #содержание_заголовок

        #set align(config.toc.align)
        #outline(
            indent: 1em,
            title: none,
        )
        
    ]
}

#let содержание() = table_of_contents()
