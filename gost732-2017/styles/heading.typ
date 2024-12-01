#import "../g7.32-2017.config.typ": config
#import "../internal-utils/utils.typ": to_str, should_be_unnumbered_heading

#let style_heading(content) = {
    // Счетчик для отсчета первого заголовка
    // Перед первым заголовком не должно быть разрывов страницы 
    let heading_pagebreak = counter("heading_pagebreak")

    set heading(numbering: config.heading.numbering)

    let try_apply_number_subheading(subheading) = {
        if counter(heading).get().at(0) != 0 {
            let heading_count = counter(heading).display() 
            return [#heading_count ] + subheading
        }
        return subheading
    }

    let try_pagebreak() = {
        if heading_pagebreak.get().at(0) != 0 {
            pagebreak()
        }
    }
    
    show heading.where(level:1): it => {
        let numbering_info = it.numbering
        // Почему-то стили корректно применяются только при использовании переводе заголовка в текст
        it = to_str(it)

        if config.heading.l1.pagebreak { try_pagebreak() }

        set text(config.heading.l1.size, weight: config.heading.l1.weight, hyphenate: false)

        let heading_number = counter(heading).display()

        // Грязный хак: получение информации из порождающей функции
        let force_numbering = false
        if type(numbering_info) == function {
            let numbering_info_res = numbering_info(none)
            if type(numbering_info_res) == dictionary {
                let number = numbering_info(none).at("force_numbering", default: none)
                if number != none {
                    force_numbering = true
                    if type(number) == int {
                        counter(heading).update(number)
                        // Почему-то обновление счетчика работает только со следующей итерации
                        heading_number = number
                    }
                }
            }
        }

        let disable_numbering = false
        if type(numbering_info) == function {
            let numbering_info_res = numbering_info(none)
            if type(numbering_info_res) == dictionary {
                let number = numbering_info(none).at("disable_numbering", default: none)
                if number != none {
                    disable_numbering = true
                }
            }
        }

        if force_numbering or (
            not disable_numbering and
            not should_be_unnumbered_heading(it)
        ) { 
            it = [ #h(config.page.parIndent) #heading_number ] + it       
        } else {
            it = upper()[ #align(center)[ #it ]]
            // Сброс счетчика для корректного определения вида подзаголовков1
            counter(heading).update(0)
        }

        par(spacing: config.heading.l1.indent)[
            #it
        ]
    }

    show heading.where(level:2): it => {
        it = to_str(it)

        if config.heading.l2.pagebreak { try_pagebreak() }

        set text(config.heading.l2.size, weight: config.heading.l2.weight, hyphenate: false)

        it = try_apply_number_subheading(it)

        if config.heading.l2.upper {
            it = upper(it)
        }

        align(config.heading.l2.align)[
            #par(spacing: config.heading.l2.indent)[
                #it
            ]
        ]
    }

    show heading.where(level:3): it => {
        it = to_str(it)

        if config.heading.l3.pagebreak { try_pagebreak() }
        
        set text(config.heading.l3.size, weight: config.heading.l3.weight, hyphenate: false)

        it = try_apply_number_subheading(it)

        if config.heading.l3.upper {
            it = upper(it)
        }

        align(config.heading.l3.align)[
            #par(spacing: config.heading.l3.indent)[
                #it
            ]
        ]
    }

    show heading.where(level:4): it => {
        it = to_str(it)

        if config.heading.l4.pagebreak { try_pagebreak() }
        
        set text(config.heading.l4.size, weight: config.heading.l4.weight, hyphenate: false)

        it = try_apply_number_subheading(it)

        if config.heading.l3.upper {
            it = upper(it)
        }

        align(config.heading.l4.align)[
            #par(spacing: config.heading.l4.indent)[
                #it
            ]
        ]
    }

    show heading: it => {
        it
        // Счет количества заголовков
        heading_pagebreak.step()
    }

    content
}
