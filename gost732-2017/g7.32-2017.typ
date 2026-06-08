#import "styles/styles.typ": *
#import "utils/utils.typ": *
#import "g7.32-2017.config.typ": *

#let gost732-2017(
    feature-table-small-spacing: false,
    feature-text-hyphenate: true,
    content
) = {
    show: style_page.with(feature-text-hyphenate);
    show: style_heading;
    show: style_list;
    show: style_toc;
    show: style_figure.with(feature-table-small-spacing);
    show: style_raw;
    show: style_table;
    show: style_eq;

    content
}

#let гост732-2017(
    фича-маленький-отступ-вокруг-таблиц: нет,
    фича-переносы-слов: да,
    content
) = gost732-2017(
    feature-table-small-spacing: фича-маленький-отступ-вокруг-таблиц,
    feature-text-hyphenate: фича-переносы-слов,
    content
)
