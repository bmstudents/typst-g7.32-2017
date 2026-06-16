// Стиль списка использованных источников по ГОСТ 7.32-2017.
// Убирает межблочные отступы внутри bibliography и оформляет каждую
// запись как абзац — за счёт чего работает красная строка 1.25 см.

#let style_bibliography(content) = {
  show bibliography: it => {
    set block(inset: 0pt)
    show block: it_block => {
      // у части блоков body == auto (не content) — их не трогаем
      if it_block.body == auto { it_block } else { par(it_block.body) }
    }
    it
  }

  content
}
