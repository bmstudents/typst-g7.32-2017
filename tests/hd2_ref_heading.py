"""hd2: @ref на раздел/заголовок печатает его номер (без слова 'раздел').

show ref в page.typ для heading проваливается в 'return it', а
set ref(supplement: it => []) убирает supplement. Ожидаем чистый номер:
'1' для раздела, '1.1' для подраздела, '2' для второго раздела.
"""
import re
import helpers as h

c = h.Checks("hd2_ref_heading")
pdf = h.compile("hd2_ref_heading.typ")
t = " ".join(h.text(pdf).split())


def ref(pre, post):
    m = re.search(re.escape(pre) + r"\s+(.+?)\s+" + re.escape(post), t)
    return m.group(1) if m else "<нет>"


r1 = ref("рздо", "рзпосле")
r11 = ref("подрдо", "подрпосле")
r2 = ref("рз2до", "рз2после")

# Главный инвариант: ссылка не должна тащить слово 'раздел'/supplement.
c.check("ref_h1_no_supplement", "раздел" not in r1.lower(),
        f"ссылка на раздел содержит слово 'раздел': '{r1}'")
c.check("ref_h1_is_1", r1 == "1", f"ссылка на раздел1 = '{r1}', ожидалось '1'")
c.check("ref_h11_is_1_1", r11 == "1.1",
        f"ссылка на подраздел = '{r11}', ожидалось '1.1'")
c.check("ref_h2_is_2", r2 == "2", f"ссылка на раздел2 = '{r2}', ожидалось '2'")

c.done()
