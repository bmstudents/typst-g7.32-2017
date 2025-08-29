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

        #pagebreak(weak: true)
        #align(center)[
            #ненумерованный_заголовок(содержание: [ ПРИЛОЖЕНИЕ #letter #toc ])[ Приложение #letter \ #strong[ #upper[ #toc ] ] ]
            Листов #context {
                counter(page).at(label(end)).at(0) - counter(page).at(label(begin)).at(0)
            }
        ] #label(begin)

        #pagebreak(weak: true)
        #content
        #pagebreak(weak: true)
        #metadata("kostyl") #label(end)
    ]
}

#let приложение(б: none, содержание: none, буква: none, content) = appendix(l: б, toc: содержание, letter: буква, content)
