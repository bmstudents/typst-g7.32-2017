#import "../internal-utils/utils.typ": to_str
#import "./heading.typ": определения_обозначения_сокращения

#let internal-definition-entry-prefix = "internal-definition-entry-"

#let definition(ref_text, definition_text) = context {
    // ключ без lower(): дедуп схлопывает только полностью идентичный текст,
    // а определения, различающиеся регистром, остаются разными записями
    let definition_key = to_str(definition_text).trim()
    let definition_index = query(selector(<internal-definition-entry>).before(here())).filter(
        entry => entry.value.key == definition_key,
    ).len()

    [
        #metadata((
            key: definition_key,
            index: definition_index,
            definition_text: definition_text,
        )) <internal-definition-entry>
    ]

    let section_rendered = query(<internal-definitions-section-rendered>).len() > 0

    if section_rendered {
        // все вхождения термина ссылаются на единственную (первую, index 0)
        // запись в разделе — повторы в разделе схлопнуты
        link(label(internal-definition-entry-prefix + definition_key + "-0"), ref_text)
    } else {
        ref_text
    }
}
#let определение(текст_ссылки, текст_определения) = definition(текст_ссылки, текст_определения)

#let definitions_designations_abbreviations_section() = context {
    // повторный вызов раздела не дублирует label (иначе ошибка «label occurs
    // multiple times»): метки ставит только первый вызов
    let already = query(selector(<internal-definitions-section-rendered>).before(here())).len() > 0
    let definition_entries = query(<internal-definition-entry>)

    // Дедупликация: один и тот же термин (повторный #определение с тем же
    // ключом) рендерим в разделе один раз. Поле index в definition() уже
    // считает порядковый номер повтора — у первого вхождения он равен 0.
    let sorted_definition_entries = definition_entries.filter(
        entry => entry.value.index == 0,
    ).sorted(
        // ё→е в ключе сортировки: иначе ё (U+0451) уезжает в конец алфавита
        key: entry => lower(to_str(entry.value.definition_text)).trim().replace("ё", "е"),
    )

    определения_обозначения_сокращения[
        #metadata(true) <internal-definitions-section-rendered>

        #set par(first-line-indent: 0em)

        #[ #h(1.25cm) В настоящем отчете о НИР применяют следующие термины с соответствующими определениями. ]
            

        #for entry in sorted_definition_entries [
            #let definition_label = internal-definition-entry-prefix + entry.value.key + "-" + str(entry.value.index)
            #if already {
                par([#entry.value.definition_text])
            } else {
                [#par([#entry.value.definition_text]) #label(definition_label)]
            }
        ]
    ]
}
#let определения_обозначения_сокращения_раздел() = definitions_designations_abbreviations_section()
