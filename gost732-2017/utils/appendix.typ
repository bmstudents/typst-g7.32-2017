#import "heading.typ": *

#let appendix(l: none, toc: none, letter: none, first-page-content: none, own-numbering: true, letter-in-figures: true, content) = {
    if l != none { letter = l }
    if letter == none { letter = "" }
    set heading(outlined: false)

    let appendix_num(.., n) = [ #if letter-in-figures [ #letter.#n ] else { n } ]

    set figure(numbering: appendix_num)

    // формулы в приложении нумеруются в его пределах, с буквой: «(А.1)».
    // (Сами формулы считаются counter(math.equation), не figure-счётчиком.)
    set math.equation(numbering: (..n) => {
        let k = n.pos().last()
        if letter-in-figures { "(" + letter + "." + str(k) + ")" } else { "(" + str(k) + ")" }
    })

    [
        #metadata("internal-appendix") <internal-appendix>

        #context {
            counter(figure.where(kind: table)).update(0)
            counter(figure.where(kind: raw)).update(0)
            counter(figure.where(kind: image)).update(0)
            counter(math.equation).update(0)
        }

        #let begin = str("internal-appendix-begin"+letter)
        #let end = str("internal-appendix-end"+letter)

        #pagebreak(weak: true)
        #align(center)[
            #ненумерованный_заголовок(содержание: [ ПРИЛОЖЕНИЕ #letter #toc ])[ 
                Приложение #letter
            ]
            #par[#strong[ #toc ]]
            #par[Листов #context {
                let minus = -1 * int(counter(page).at(label(end)) != counter(page).final())
                counter(page).at(label(end)).at(0) - counter(page).at(label(begin)).at(0) + minus
            }]
        ] #label(begin)

        #if first-page-content != none {
            first-page-content
        }

        #pagebreak(weak: true)

        // Собственная нумерация
        #set page(
            footer: [
                #set text(size: config.page.textSize)
                #set align(config.page.alignNum)
                #context[#if own-numbering {
                    counter(page).get().at(0) - counter(page).at(label(begin)).at(0)
                } else {
                    counter(page).get().at(0)
                }]
            ]
        )
        

        #content
        // метка конца — ДО финального разрыва, чтобы она оставалась на
        // последней странице ЭТОГО приложения и не протекала на следующее
        // (иначе «Листов N» завышается у не-последнего приложения)
        #metadata("kostyl") #label(end)
        #pagebreak(weak: true)
    ]
}

#let приложение(
    б: none,
    содержание: none,
    буква: none,
    контент-первой-страницы: none,
    собственная-нумерация: true,
    буква-в-иллюстрациях: true,
    content
) = appendix(
    l: б,
    toc: содержание,
    letter: буква,
    first-page-content: контент-первой-страницы,
    own-numbering: собственная-нумерация,
    letter-in-figures: буква-в-иллюстрациях,
    content
)
