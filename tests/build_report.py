#!/usr/bin/env python3
"""Собирает единый отчёт: перед pdf каждого теста вставляет лист-пояснение
(имя теста, что проверяет — из докстринга, список проверок c.check, статус
PASS/FAIL по прогону). Результат — tests/.out/report.pdf.

Запуск: python3 build_report.py   (нативно, typst+pdfunite берутся env-независимо)
"""
import ast
import glob
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import helpers as h

PDFUNITE = h._bin("pdfunite")
SKIP = {"helpers.py", "run_all.py", "build_report.py"}


def esc(s):
    """Экранирование под typst-строку."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def parse(py):
    """Из .py: docstring, имя suite, имена проверок."""
    src = open(py, encoding="utf-8").read()
    tree = ast.parse(src)
    doc = " ".join((ast.get_docstring(tree) or "").split())
    suite = os.path.basename(py)[:-3]
    checks = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            attr = getattr(node.func, "attr", None) or getattr(node.func, "id", None)
            if attr == "Checks" and node.args and isinstance(node.args[0], ast.Constant):
                suite = node.args[0].value
            if attr == "check" and node.args and isinstance(node.args[0], ast.Constant):
                checks.append(str(node.args[0].value))
    return doc, suite, checks


def run_status(py):
    r = subprocess.run([sys.executable, os.path.basename(py)],
                       capture_output=True, text=True, cwd=h.TESTS_DIR)
    return r.stdout.count("PASS "), r.stdout.count("FAIL ")


def make_cover(stem, doc, suite, checks, npass, nfail):
    ok = nfail == 0
    checks_typ = ", ".join('"%s"' % esc(c) for c in checks)
    typ = f'''#set page(paper: "a4", margin: 2.5cm, footer: none)
#set text(font: "Times New Roman", size: 13pt, lang: "ru")
#v(3cm)
#align(center)[
  #text(size: 11pt, fill: luma(130))[ТЕСТ]
  #v(3mm)
  #text(size: 24pt, weight: "bold")[#raw("{esc(suite)}")]
]
#v(1cm)
#text(size: 11pt, fill: luma(110))[ЧТО ПРОВЕРЯЕТ]
#v(2mm)
#par(justify: true)[#"{esc(doc) or "—"}"]
#v(8mm)
#text(size: 11pt, fill: luma(110))[ПРОВЕРКИ — {len(checks)}]
#v(2mm)
#for c in ({checks_typ}{"," if len(checks)==1 else ""}) [ #sym.bullet #raw(c) \\ ]
#v(1cm)
#align(center)[
  #text(size: 18pt, weight: "bold", fill: {"rgb(40,140,60)" if ok else "rgb(190,40,40)"})[
    {"ПРОЙДЕН" if ok else "ПРОВАЛЕН"} — {npass}/{npass + nfail}
  ]
]
'''
    cpath = os.path.join(h.OUT, f"_cover_{stem}.typ")
    open(cpath, "w", encoding="utf-8").write(typ)
    out = os.path.join(h.OUT, f"_cover_{stem}.pdf")
    r = subprocess.run([h.TYPST, "compile", "--root", h.REPO, cpath, out],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"cover {stem} failed:\n{r.stderr}")
    return out


def process(py):
    stem = os.path.basename(py)[:-3]
    doc, suite, checks = parse(py)
    npass, nfail = run_status(py)
    cover = make_cover(stem, doc, suite, checks, npass, nfail)
    # pdf'ы теста: одноимённый + <stem>_*.pdf (multi-pdf тесты)
    pdfs = sorted(set(glob.glob(os.path.join(h.OUT, f"{stem}.pdf")) +
                      glob.glob(os.path.join(h.OUT, f"{stem}_*.pdf"))))
    return [cover] + pdfs, suite, npass, nfail


def main():
    files = sorted(f for f in glob.glob(os.path.join(h.TESTS_DIR, "*.py"))
                   if os.path.basename(f) not in SKIP)
    print(f"тестов: {len(files)}")
    with ThreadPoolExecutor(max_workers=12) as ex:
        results = list(ex.map(process, files))
    order = []
    npass = nfail = 0
    for pdfs, suite, p, f in results:
        order += pdfs
        npass += p
        nfail += f
    report = os.path.join(h.OUT, "report.pdf")
    # файлов >256 → склеиваем инкрементально пачками (каждый pdfunite
    # открывает ≤ batch+1 файлов, не упираясь в ulimit -n)
    tmp = os.path.join(h.OUT, "_acc.pdf")
    batch = 120
    acc = None
    for i in range(0, len(order), batch):
        chunk = order[i:i + batch]
        ins = ([acc] if acc else []) + chunk
        dst = report if i + batch >= len(order) else tmp
        r = subprocess.run([PDFUNITE] + ins + [dst + ".new"], capture_output=True, text=True)
        if not os.path.exists(dst + ".new"):
            raise RuntimeError(f"pdfunite batch failed:\n{r.stderr}")
        os.replace(dst + ".new", dst)
        acc = dst
    print(f"covers+pdfs: {len(order)} | проверок {npass} ok / {nfail} fail")
    print(f"report: {report}")


if __name__ == "__main__":
    main()
