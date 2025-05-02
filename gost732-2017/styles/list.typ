#import "../g7.32-2017.config.typ":config

#let style_list(content) = {
    set list(indent: 0pt)
    
    show list: it => {
        h(-config.page.parIndent)
        for phase in it.children [
            #h(config.page.parIndent) -- #phase.body \
        ]
    }

    set enum(indent: 0pt)

    show enum: it => {
        let i = 1
        h(-config.page.parIndent)
        for phase in it.children [
            #h(config.page.parIndent) #i) #phase.body \
            #{i=i+1}
        ]
    }

    content
}
