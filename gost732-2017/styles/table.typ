#import "../g7.32-2017.config.typ": config

#let style_table(content) = {
    show figure.where(
        kind: table
    ): it => {
        set block(breakable: true)
        set figure.caption(position: top)
        show figure.caption: set align(left)

        it
    }

    set table.cell(breakable: true)

    set table(inset: config.figure.inset)

    // В таблицах перенос слов по слогам не применяется (ГОСТ): в узких
    // ячейках он даёт «логи-ка», на что ругается TestVkr. Перенос в
    // обычном тексте при этом сохраняется.
    show table: set text(hyphenate: false)

    content
}
