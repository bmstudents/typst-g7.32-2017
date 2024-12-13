#import "styles/styles.typ": *
#import "utils/utils.typ": *

#let gost732-2017(content) = {
    show: style_page;
    show: style_heading;
    show: style_list;
    show: style_toc;
    show: style_figure;
    content
}

#let гост732-2017(content) = gost732-2017(content)
