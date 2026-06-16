"""hf4_doc_metadata: #set document(title:, author:) -> метаданные PDF.

Пакет gost732-2017 не вызывает #set document сам, поэтому пользовательские
title/author должны без искажений попасть в метаданные PDF (Title/Author).
Если бы пакет где-то перетирал document — этот тест бы это поймал.

Читаем метаданные через pdfinfo.
"""
import subprocess
import helpers as h

c = h.Checks("hf4_doc_metadata")
pdf = h.compile("hf4_doc_metadata.typ")

info = subprocess.run([h.PDFINFO, pdf], capture_output=True, text=True).stdout
fields = {}
for line in info.splitlines():
    if ":" in line:
        k, _, v = line.partition(":")
        fields[k.strip().lower()] = v.strip()

c.check(
    "title_set",
    fields.get("title") == "Заголовок Отчёта НИР",
    f"Title метаданных != заданному. Получено: {fields.get('title')!r}",
)
c.check(
    "author_set",
    fields.get("author") == "Иванов И.И.",
    f"Author метаданных != заданному. Получено: {fields.get('author')!r}",
)
# Содержимое тоже на месте.
norm = " ".join(h.text(pdf).split())
c.check(
    "body_compiled",
    "РЕФЕРАТ" in norm,
    f"тело документа не отрисовалось:\n  {norm[:160]}",
)

c.done()
