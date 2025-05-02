#import "heading.typ": *

#let appendix(l: none, toc: none, letter: none, content) = {
    if l != none { letter = l }
    if letter == none { letter = "" }
    set heading(outlined: false)

    let appendix_num(.., n) = [#letter.#n]

    set figure(numbering: appendix_num)

    [
        #metadata("internal-appendix") <internal-appendix>

        #context {
            counter(figure.where(kind: table)).update(0)
            counter(figure.where(kind: raw)).update(0)
            counter(figure.where(kind: image)).update(0)
            counter(figure.where(kind: math.equation)).update(0)
        }

        #let begin = str("internal-appendix-begin"+letter)
        #let end = str("internal-appendix-end"+letter)

        #align(center)[
            #ненумерованный_заголовок(содержание: [ ПРИЛОЖЕНИЕ #letter #toc])[ = Приложение #letter ]
            #strong[ #upper[ #toc ] ]
            \ Листов #context { 
                let minus = -1 * int(counter(page).at(label(end)) != counter(page).final())
                counter(page).at(label(end)).at(0) - counter(page).at(label(begin)).at(0) + minus
            }
        ] #label(begin)

        #set page(
            footer: [
                #set text(size: config.page.textSize)
                #set align(config.page.alignNum)
                #context { counter(page).get().at(0) - counter(page).at(label(begin)).at(0) }
            ]
        )

        #content
        #pagebreak(weak: true)
        #metadata("kostyl") #label(end)
    ]
}

#let приложение(б: none, содержание: none, буква: none, content) = appendix(l: б, toc: содержание, letter: буква, content)
