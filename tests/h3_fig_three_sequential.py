"""h3 РИСУНКИ: три последовательных рисунка нумеруются «Рисунок 1/2/3» строго по порядку.

Три rect подряд с метками тел ТЕЛОA, ТЕЛОB, ТЕЛОC. Проверяем сквозную нумерацию
counter(figure.kind:image) и согласованность визуального порядка (по y) с номерами.

ИНВАРИАНТЫ:
  1. ровно три подписи «Рисунок», их номера в порядке появления = ['1','2','3'];
  2. подписи идут сверху вниз: y(Рис1) < y(Рис2) < y(Рис3) (нет перестановки блоков);
  3. порядок тел ТЕЛОA<ТЕЛОB<ТЕЛОC по y совпадает с порядком подписей,
     и каждое тело выше СВОЕЙ подписи (тело_k.yMax < подпись_k.yMin) —
     т.е. рисунок и его номер не перемешались между собой.
"""
import helpers as h

c = h.Checks("h3_fig_three_sequential")
pdf = h.compile("h3_fig_three_sequential.typ")
ws = h.words(pdf)

# Подписи «Рисунок» по порядку появления (документ-ордер pdftotext = сверху вниз
# в пределах страницы; здесь всё на одной странице).
caps = [w for w in ws if w[5] == "Рисунок"]

c.check("three_captions", len(caps) == 3,
        f"подписей «Рисунок» = {len(caps)}, ожидалось 3")

# Номер сразу справа от слова «Рисунок» на той же строке.
def number_after(cap):
    same_line = [w for w in ws if w[0] == cap[0] and abs(w[2] - cap[2]) < 2.0
                 and w[1] > cap[3] and w[5] in ("1", "2", "3", "4", "5")]
    same_line.sort(key=lambda w: w[1])
    return same_line[0][5] if same_line else None


if len(caps) == 3:
    nums = [number_after(cp) for cp in caps]
    # 1. сквозная нумерация 1,2,3 в порядке появления
    c.check("numbering_1_2_3", nums == ["1", "2", "3"],
            f"номера рисунков в порядке появления = {nums}, ожидалось ['1','2','3']")
    # 2. подписи строго сверху вниз
    ys = [cp[2] for cp in caps]
    c.check("captions_top_to_bottom", ys[0] < ys[1] < ys[2],
            f"подписи не по возрастанию y: {[round(y,1) for y in ys]}")

# 3. тела в том же порядке и каждое выше своей подписи
bodies = {}
for tag in ("ТЕЛОA", "ТЕЛОB", "ТЕЛОC"):
    hit = [w for w in ws if w[5] == tag]
    bodies[tag] = hit[0] if len(hit) == 1 else None

if all(bodies.values()) and len(caps) == 3:
    ba, bb, bc = bodies["ТЕЛОA"], bodies["ТЕЛОB"], bodies["ТЕЛОC"]
    order_ok = ba[2] < bb[2] < bc[2]
    pair_ok = (ba[4] < caps[0][2] and bb[4] < caps[1][2] and bc[4] < caps[2][2])
    c.check("bodies_match_caption_order", order_ok and pair_ok,
            f"тела/подписи рассогласованы: yТел={[round(ba[2],1),round(bb[2],1),round(bc[2],1)]}, "
            f"yПодп={[round(caps[0][2],1),round(caps[1][2],1),round(caps[2][2],1)]}, "
            f"order_ok={order_ok} pair_ok={pair_ok}")
else:
    found = {k: (v is not None) for k, v in bodies.items()}
    c.check("bodies_match_caption_order", False,
            f"не все тела найдены однозначно: {found}")

c.done()
