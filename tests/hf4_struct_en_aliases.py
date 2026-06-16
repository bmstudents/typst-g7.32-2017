"""hf4_struct_en_aliases: английские алиасы структурных констант.

Каждый английский алиас должен давать ТОТ ЖЕ прописной русский заголовок,
что и русская константа. Имена алиасов берём как они реально экспортированы
из gost732-2017/utils/heading.typ (в т.ч. опечатка 'conslusion').

Алиас #abbreviations_and_designations ('Перечень сокращений и ссылок')
проверяется тем же инвариантом — и падает по той же причине, что и в
hf4_struct_perechen (рассинхрон константы и регэкспа).
"""
import helpers as h

c = h.Checks("hf4_struct_en_aliases")
pdf = h.compile("hf4_struct_en_aliases.typ")
norm = " ".join(h.text(pdf).split())

cases = {
    "abstract": "РЕФЕРАТ",
    "introduction": "ВВЕДЕНИЕ",
    "conslusion": "ЗАКЛЮЧЕНИЕ",
    "terms_and_definitions": "ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ",
    "authors_list": "СПИСОК ИСПОЛНИТЕЛЕЙ",
}
for alias, txt in cases.items():
    c.check(
        f"alias_{alias}",
        txt in norm,
        f"англ. алиас #{alias} не дал прописной заголовок '{txt}':\n  {norm[:200]}",
    )

# abbreviations_and_designations — тот же баг, что и русский алиас.
c.check(
    "alias_abbreviations_and_designations",
    "ПЕРЕЧЕНЬ СОКРАЩЕНИЙ И ССЫЛОК" in norm,
    "англ. алиас #abbreviations_and_designations не дал прописной\n"
    "  заголовок 'ПЕРЕЧЕНЬ СОКРАЩЕНИЙ И ССЫЛОК'.\n"
    "  Тот же рассинхрон: should_be_upper_heading ждёт 'перечень сокращений\n"
    "  и обозначений', а константа — 'Перечень сокращений и ССЫЛОК'\n"
    "  (gost732-2017/internal-utils/utils.typ vs utils/heading.typ).\n"
    f"  Текст PDF: {norm[:200]}",
)

c.done()
