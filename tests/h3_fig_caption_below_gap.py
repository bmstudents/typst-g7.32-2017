"""h3 РИСУНКИ: подпись расположена ПОД телом рисунка с НЕнулевым зазором.

По ГОСТ 7.32 подпись «Рисунок N – …» ставится под иллюстрацией, отделённая
интервалом (config.page.spacing == 1.06em ≈ 14.8pt). Тело rect(8cm×5cm) несёт
две текст-метки: ВЕРХТЕЛА (верх тела) и НИЗТЕЛА (низ тела) — по ним измеряем
вертикальную протяжённость тела, тк сам прямоугольник в текстовый слой не попадает.

ИНВАРИАНТ:
  yMin(«Рисунок») > yMax(НИЗТЕЛА)           — подпись строго ниже низа тела;
  zазор = yMin(«Рисунок») − yMax(НИЗТЕЛА) > 0 — есть положительный интервал;
  НИЗТЕЛА ниже ВЕРХТЕЛА                      — метки тела согласованы (sanity).
"""
import helpers as h

c = h.Checks("h3_fig_caption_below_gap")
pdf = h.compile("h3_fig_caption_below_gap.typ")
ws = h.words(pdf)


def one(word):
    hits = [w for w in ws if w[5] == word]
    return hits[0] if len(hits) == 1 else None


top = one("ВЕРХТЕЛА")
bot = one("НИЗТЕЛА")
cap = one("Рисунок")

c.check("markers_and_caption_unique",
        top is not None and bot is not None and cap is not None,
        f"не нашёл по одному разу метки/подпись: top={top} bot={bot} cap={cap}")

if top and bot and cap:
    # sanity: всё на одной странице (иначе остальные сравнения y бессмысленны)
    same_page = top[0] == bot[0] == cap[0]
    c.check("single_page", same_page,
            f"страницы разные: top={top[0]} bot={bot[0]} cap={cap[0]}")

    if same_page:
        # 1. метки тела согласованы по вертикали
        c.check("body_markers_ordered", bot[4] > top[2],
                f"НИЗТЕЛА yMax={bot[4]:.1f} должен быть ниже ВЕРХТЕЛА yMin={top[2]:.1f}")
        # 2. подпись строго ниже низа тела
        c.check("caption_below_body", cap[2] > bot[4],
                f"подпись yMin={cap[2]:.1f} НЕ ниже низа тела yMax={bot[4]:.1f}")
        # 3. зазор между телом и подписью положителен
        gap = cap[2] - bot[4]
        c.check("positive_gap", gap > 0.5,
                f"зазор тело→подпись = {gap:.2f}pt, ожидался > 0.5pt")

c.done()
