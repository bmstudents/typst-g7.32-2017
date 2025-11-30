#let style_bib(content) = {
    // set bibliography(
    //     title: none,
    //     style: "gost-r-705-2008-numeric",
    //     full: true
    // )

    context {
        let custom_bibliography = query(<gost732-2017-feature-custom-bibliography>).last().value;
        let number_delimiter = query(<gost732-2017-feature-custom-bibliography-number-delimiter>).last().value;

        let csl = str(read("g-bib.csl")).replace("{NUMBER_DELIMITER}", number_delimiter);
        set bibliography(style: bytes(csl));
        show bibliography: it_bib => {
            set block(inset: 0pt)
            show block: it_block => {
                par(it_block.body)
            }
            it_bib
        }
    }
    
}
