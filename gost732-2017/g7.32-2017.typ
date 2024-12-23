#import "styles/styles.typ": *
#import "utils/utils.typ": *
#import "g7.32-2017.config.typ": *

#let gost732-2017(content) = {
    show: style_page;
    show: style_heading;
    show: style_list;
    show: style_toc;
    show: style_figure;
    show: style_raw;
    show: style_table;
    content
}

#let гост732-2017(content) = gost732-2017(content)
