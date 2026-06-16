"""Хелпер для измерения РЕАЛЬНОГО ИНКА (а не только bbox слов pdftotext).

Зачем: фича `фича-маленький-отступ-вокруг-таблиц: да` добавляет отрицательные
v(-0.5em) вокруг тела/подписи таблиц, листингов, рисунков. Тело листинга в
этом пакете оборачивается в table() с рамкой (styles/raw.typ), а подпись —
это box(width:100%). Слова pdftotext не видят РАМКУ блока: между словом
подписи и ПЕРВЫМ СЛОВОМ тела зазор может оставаться положительным, тогда как
верхняя граница рамки тела уже наехала на подпись. Поэтому для honest-проверки
наезда нужен растровый слой: рендерим .typ в PNG (typst --ppi) и ищем
горизонтальные «полосы инка» (ink bands) — связные по вертикали диапазоны
строк, где есть тёмные пиксели. Слипание двух соседних блоков в одну полосу =
наезд.

Зависимости: typst (рендер PNG), Pillow (анализ растра).
"""
import os
import subprocess

import helpers as h

try:
    from PIL import Image
except Exception as e:  # pragma: no cover
    Image = None
    _PIL_ERR = e


def render_png(typ_path, ppi=150):
    """Компилирует .typ в PNG нашей версией пакета. Возвращает путь к png.

    Для одностраничных документов typst пишет ровно один файл .png.
    """
    typ_path = os.path.join(h.TESTS_DIR, typ_path) if not os.path.isabs(typ_path) else typ_path
    name = os.path.splitext(os.path.basename(typ_path))[0]
    png = os.path.join(h.OUT, name + ".png")
    r = subprocess.run(
        [h.TYPST, "compile", "--root", h.REPO, "--ppi", str(ppi), typ_path, png],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(f"compile(png) failed for {typ_path}:\n{r.stderr}")
    return png, ppi


def ink_bands(png_path, ppi, x_lo_pt=None, x_hi_pt=None,
              y_lo_pt=None, y_hi_pt=None, thr=128, merge_px=2):
    """Связные вертикальные полосы инка в координатах PT (1pt = ppi/72 px).

    x_lo/x_hi/y_lo/y_hi — необязательное окно отбора (в pt), чтобы исключить
    номер страницы, заголовок раздела и т.п. Полосы, разделённые <= merge_px
    пустыми строками, объединяются (антиалиасинг сглаживает рамки в 1-2px).

    Возвращает список (y0_pt, y1_pt) сверху вниз.
    """
    if Image is None:  # pragma: no cover
        raise RuntimeError(f"Pillow недоступен: {_PIL_ERR}")
    im = Image.open(png_path).convert("L")
    w, ht = im.size
    px = im.load()
    scale = 72.0 / ppi  # px -> pt
    inv = ppi / 72.0     # pt -> px

    x0 = 0 if x_lo_pt is None else max(0, int(x_lo_pt * inv))
    x1 = w if x_hi_pt is None else min(w, int(x_hi_pt * inv))
    yy0 = 0 if y_lo_pt is None else max(0, int(y_lo_pt * inv))
    yy1 = ht if y_hi_pt is None else min(ht, int(y_hi_pt * inv))

    dark_rows = []
    for y in range(yy0, yy1):
        has = False
        for x in range(x0, x1):
            if px[x, y] < thr:
                has = True
                break
        if has:
            dark_rows.append(y)

    bands = []
    cur = None
    prev = None
    for y in dark_rows:
        if cur is None:
            cur = [y, y]
        elif y - prev <= merge_px:
            cur[1] = y
        else:
            bands.append((cur[0] * scale, cur[1] * scale))
            cur = [y, y]
        prev = y
    if cur is not None:
        bands.append((cur[0] * scale, cur[1] * scale))
    return bands


def widest_dark_rows(png_path, ppi, min_span_pt=150, y_lo_pt=None, y_hi_pt=None, thr=128):
    """Строки-«линейки»: где тёмные пиксели тянутся шире min_span_pt (рамки таблиц).

    Возвращает список y_pt таких строк (отсортирован). По ним ловим ВЕРХНЮЮ
    границу рамки тела листинга/таблицы — именно она наезжает на подпись.
    """
    if Image is None:  # pragma: no cover
        raise RuntimeError(f"Pillow недоступен: {_PIL_ERR}")
    im = Image.open(png_path).convert("L")
    w, ht = im.size
    px = im.load()
    scale = 72.0 / ppi
    inv = ppi / 72.0
    yy0 = 0 if y_lo_pt is None else max(0, int(y_lo_pt * inv))
    yy1 = ht if y_hi_pt is None else min(ht, int(y_hi_pt * inv))
    res = []
    for y in range(yy0, yy1):
        xs = [x for x in range(w) if px[x, y] < thr]
        if xs and (max(xs) - min(xs)) * scale >= min_span_pt:
            res.append(y * scale)
    return res
