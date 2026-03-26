#import "../internal-utils/utils.typ": to_str
#import "./heading.typ": определения_обозначения_сокращения

#let internal-definition-entry-prefix = "internal-definition-entry-"

#let definition(ref_text, definition_text) = context {
    let definition_key = lower(to_str(definition_text)).trim()
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
        link(label(internal-definition-entry-prefix + definition_key + "-" + str(definition_index)), ref_text)
    } else {
        ref_text
    }
}
#let определение(текст_ссылки, текст_определения) = definition(текст_ссылки, текст_определения)

#let definitions_designations_abbreviations_section() = context {
    let definition_entries = query(<internal-definition-entry>)

    let sorted_definition_entries = definition_entries.sorted(
        key: entry => lower(to_str(entry.value.definition_text)).trim(),
    )

    определения_обозначения_сокращения[
        #metadata(true) <internal-definitions-section-rendered>
        #set par(first-line-indent: 0em)

        #for entry in sorted_definition_entries [
            #let definition_label = internal-definition-entry-prefix + entry.value.key + "-" + str(entry.value.index)
            #par([#entry.value.definition_text]) #label(definition_label)
        ]
    ]
}
#let определения_обозначения_сокращения_раздел() = definitions_designations_abbreviations_section()
