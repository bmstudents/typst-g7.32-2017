#import "styles/styles.typ": *
#import "utils/utils.typ": *
#import "g7.32-2017.config.typ": *

#let gost732-2017(
    feature-table-small-spacing: false,
    feature-text-hyphenate: true,
    feature-space-before-subheading: false,
    feature-nonbreaking-values: false,
    content
) = {
    show: style_page.with(feature-text-hyphenate);
    show: style_heading.with(feature-space-before-subheading);
    show: style_list;
    show: style_toc;
    show: style_figure.with(feature-table-small-spacing);
    show: style_raw;
    show: style_table;
    show: style_eq;
    show: style_bibliography;
    show: if feature-nonbreaking-values { style_typography } else { (c) => c };

    content
}

#let гост732-2017(
    фича-маленький-отступ-вокруг-таблиц: нет,
    фича-переносы-слов: да,
    фича-отступ-перед-подразделом: нет,
    фича-неразрывные-величины: нет,
    content
) = gost732-2017(
    feature-table-small-spacing: фича-маленький-отступ-вокруг-таблиц,
    feature-text-hyphenate: фича-переносы-слов,
    feature-space-before-subheading: фича-отступ-перед-подразделом,
    feature-nonbreaking-values: фича-неразрывные-величины,
    content
)
