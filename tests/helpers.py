"""Общие хелперы для тест-харнесса gost732-2017.

Каждый тест компилирует свой .typ нашей dev-версией пакета и проверяет
результат: либо текстовый слой (pdftotext), либо координаты слов
(pdftotext -bbox). Зависимости: typst 0.14.2, pdftotext (poppler).
"""
import os
import re
import shutil
import subprocess

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TESTS_DIR)
OUT = os.path.join(TESTS_DIR, ".out")
os.makedirs(OUT, exist_ok=True)


def _bin(name):
    """Находит бинарь кроссплатформенно, не завися от среды запуска.

    Порядок: явный оверрайд через env (TYPST_BIN / PDFTOTEXT_BIN) → PATH →
    типичные локации для любой ОС (linux/macOS/cargo/snap/macports). Нужно,
    тк неинтерактивный ssh не подхватывает пользовательский PATH (на macOS —
    /opt/homebrew/bin, на linux — ~/.local/bin и т.п.)."""
    env = os.environ.get(name.upper() + "_BIN")
    if env and os.path.exists(env):
        return env
    p = shutil.which(name)
    if p:
        return p
    home = os.path.expanduser("~")
    exe = name + (".exe" if os.name == "nt" else "")
    candidates = (
        os.path.join(home, "bin"),
        os.path.join(home, ".local", "bin"),
        os.path.join(home, ".cargo", "bin"),
        "/opt/homebrew/bin",   # macOS (Apple Silicon, brew)
        "/usr/local/bin",      # macOS (Intel, brew) / linux
        "/usr/bin", "/bin",
        "/snap/bin",           # linux snap
        "/opt/local/bin",      # macports
    )
    for d in candidates:
        cand = os.path.join(d, exe)
        if os.path.exists(cand):
            return cand
    return name


TYPST = _bin("typst")
PDFTOTEXT = _bin("pdftotext")
PDFINFO = _bin("pdfinfo")
PDFFONTS = _bin("pdffonts")


def compile(typ_path):
    """Компилирует .typ в pdf нашей версией пакета. Бросает на ошибке."""
    typ_path = os.path.join(TESTS_DIR, typ_path) if not os.path.isabs(typ_path) else typ_path
    name = os.path.splitext(os.path.basename(typ_path))[0]
    pdf = os.path.join(OUT, name + ".pdf")
    r = subprocess.run(
        [TYPST, "compile", "--root", REPO, typ_path, pdf],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(f"compile failed for {typ_path}:\n{r.stderr}")
    return pdf


def text(pdf):
    """Весь текстовый слой pdf одной строкой (с \\n)."""
    return subprocess.run([PDFTOTEXT, pdf, "-"], capture_output=True).stdout.decode("utf-8")


def words(pdf):
    """Список слов с координатами: [(page, x0, y0, x1, y1, word), ...]."""
    out = subprocess.run([PDFTOTEXT, "-bbox", pdf, "-"], capture_output=True, text=True).stdout
    res = []
    for pi, p in enumerate(re.split(r"<page", out)[1:], 1):
        for x0, y0, x1, y1, w in re.findall(
            r'xMin="([0-9.]+)" yMin="([0-9.]+)" xMax="([0-9.]+)" yMax="([0-9.]+)">([^<]+)<', p
        ):
            res.append((pi, float(x0), float(y0), float(x1), float(y1), w.strip()))
    return res


def page_count(pdf):
    return len(re.split(r"<page", subprocess.run([PDFTOTEXT, "-bbox", pdf, "-"],
                                                 capture_output=True, text=True).stdout)) - 1


def first_word(pdf, page):
    """Первое (самое верхнее) слово на странице: (y, word) или None."""
    ws = [w for w in words(pdf) if w[0] == page]
    if not ws:
        return None
    top = min(ws, key=lambda t: t[2])
    return (top[2], top[5])


def footer_word(pdf, page):
    """Самое нижнее слово страницы (обычно номер) или None."""
    ws = [w for w in words(pdf) if w[0] == page]
    if not ws:
        return None
    return max(ws, key=lambda t: t[2])[5]


def y_of(pdf, word, nth=1, page=None):
    """yMin n-го вхождения слова (опц. на конкретной странице)."""
    hits = [w for w in words(pdf) if w[5] == word and (page is None or w[0] == page)]
    return hits[nth - 1][2] if len(hits) >= nth else None


class Checks:
    """Накопитель проверок одного теста: 2-3 check на фичу."""
    def __init__(self, suite):
        self.suite = suite
        self.fails = 0
        self.total = 0

    def check(self, name, cond, detail=""):
        self.total += 1
        if cond:
            print(f"PASS {self.suite}::{name}")
        else:
            self.fails += 1
            print(f"FAIL {self.suite}::{name} — {detail}")

    def done(self):
        import sys
        print(f"--- {self.suite}: {self.total - self.fails}/{self.total} ---")
        sys.exit(1 if self.fails else 0)
