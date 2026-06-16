"""hd3: нумерация страниц в многостраничном документе (10+ страниц).

Инварианты:
 - footer каждой страницы — арабский номер, равный её порядковому номеру;
 - номера монотонно растут 1,2,3,...;
 - двузначные номера (>=10) по центру не съезжают: центр номера совпадает
   с центром одноразрядных в пределах допуска.
"""
import helpers as h

c = h.Checks("hd3_page_footer_monotonic")
pdf = h.compile("hd3_page_footer_monotonic.typ")
n = h.page_count(pdf)

c.check("at_least_10_pages", n >= 10, f"страниц {n}, нужно >=10 для двузначных")

# footer каждой страницы == её номер, монотонно
nums = []
ok_seq = True
for p in range(1, n + 1):
    fw = h.footer_word(pdf, p)
    nums.append(fw)
    if not (fw and fw.isdigit() and int(fw) == p):
        ok_seq = False
c.check("footer_is_page_number", ok_seq,
        f"footer != номер страницы; последовательность: {nums}")

# отдельно: монотонность арабских
digits = [int(x) for x in nums if x and x.isdigit()]
c.check("monotonic", digits == sorted(digits) and len(set(digits)) == len(digits),
        f"номера не монотонны/повторяются: {digits}")

# центрирование: возьмём bbox футера на одноразрядной (стр.5) и
# двузначной (стр.10+) страницах, сравним центр по X.
def footer_center_x(page):
    ws = [w for w in h.words(pdf) if w[0] == page]
    if not ws:
        return None
    fw = max(ws, key=lambda t: t[4])  # самое нижнее по yMax
    return (fw[1] + fw[3]) / 2.0

cx_single = footer_center_x(5)
cx_double = footer_center_x(n)  # последняя точно двузначная (>=12)
c.check("two_digit_centered",
        cx_single is not None and cx_double is not None
        and abs(cx_single - cx_double) <= 3.0,
        f"центр двузначного номера съехал: single={cx_single}, double={cx_double}")
c.done()
