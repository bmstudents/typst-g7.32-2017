"""h3 РИСУНКИ: повёрнуто:true — тело на 90°, а подпись «Рисунок N» остаётся ГОРИЗОНТАЛЬНОЙ.

img() оборачивает в rotate(-90deg) только data (тело), но НЕ caption. Значит
текст подписи должен идти нормально слева-направо, а текст-метка ВНУТРИ тела —
повёрнуто (вертикально). Геометрию различаем по форме bbox каждого слова:
горизонтальный текст → width > height; повёрнутый на 90° → height > width.

ИНВАРИАНТЫ:
  1. слово «Рисунок» горизонтально: width(bbox) > height(bbox) (и заметно: >2:1);
  2. метка тела ПОВТЕЛО повёрнута: height(bbox) > width(bbox) — тело реально на 90°;
  3. подпись ниже тела на той же странице (yMin подписи > yMax тела) —
     подпись под рисунком, как требует ГОСТ, а не сбоку/над.
"""
import helpers as h

c = h.Checks("h3_fig_rotated_caption_horizontal")
pdf = h.compile("h3_fig_rotated_caption_horizontal.typ")
ws = h.words(pdf)


def one(word):
    hits = [w for w in ws if w[5] == word]
    return hits[0] if len(hits) == 1 else None


cap = one("Рисунок")
body = one("ПОВТЕЛО")

c.check("words_present", cap is not None and body is not None,
        f"подпись/метка тела не найдены однозначно: cap={cap} body={body}")

if cap and body:
    cap_w, cap_h = cap[3] - cap[1], cap[4] - cap[2]
    bod_w, bod_h = body[3] - body[1], body[4] - body[2]

    # 1. подпись «Рисунок» — горизонтальная (широкая, низкая)
    c.check("caption_horizontal", cap_w > 2 * cap_h,
            f"«Рисунок» bbox {cap_w:.1f}×{cap_h:.1f} (W×H): подпись не выглядит "
            f"горизонтальной (ожидалось W > 2·H). Возможно, повернулась вместе с телом.")
    # 2. тело реально повёрнуто на 90° — метка вертикальна (высокая, узкая)
    c.check("body_rotated", bod_h > bod_w,
            f"метка тела ПОВТЕЛО bbox {bod_w:.1f}×{bod_h:.1f} (W×H): тело не повёрнуто "
            f"(ожидалось H > W при повернуто:true)")
    # 3. подпись под телом на одной странице
    same = cap[0] == body[0]
    c.check("caption_below_rotated_body", same and cap[2] > body[4],
            f"подпись стр{cap[0]} yMin={cap[2]:.1f}, тело стр{body[0]} yMax={body[4]:.1f}: "
            f"подпись не строго ниже тела")

c.done()
