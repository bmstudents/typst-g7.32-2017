"""hf2: номер страницы — по центру ПОЛОСЫ НАБОРА, а не центра листа.

Поля: left 30мм=85.04pt, right 15мм=42.52pt. Полоса набора: [85.04, 552.76].
Её центр = 318.9pt. Центр ЛИСТА A4 = 595.276/2 = 297.6pt. Это две РАЗНЫЕ точки
(разница ~21pt из-за асимметричных полей по ГОСТ). Номер обязан стоять в 318.9,
а не в 297.6 и не у края.
"""
import helpers as h

c = h.Checks("hf2_footer_centered_content")
pdf = h.compile("hf2_footer_centered_content.typ")

PAGE_W = 595.276
LEFT = 85.04            # 30мм
RIGHT_EDGE = PAGE_W - 42.52   # правый край полосы = 552.76
CONTENT_CX = (LEFT + RIGHT_EDGE) / 2   # 318.9
SHEET_CX = PAGE_W / 2                  # 297.6

for p in (1, 2):
    nums = [w for w in h.words(pdf) if w[0] == p and w[2] > 700 and w[5].isdigit()]
    c.check(f"p{p}_footer_present", len(nums) == 1,
            f"стр.{p}: ждём ровно один нижний номер, найдено {[w[5] for w in nums]}")
    if not nums:
        continue
    f = nums[0]
    cx = (f[1] + f[3]) / 2

    # Центр номера совпадает с центром полосы набора (318.9), допуск 5pt.
    c.check(f"p{p}_at_content_center",
            abs(cx - CONTENT_CX) < 5,
            f"стр.{p}: cx номера={cx:.1f}, ждём {CONTENT_CX:.1f} (центр полосы набора)")

    # И НЕ совпадает с центром листа (297.6): номер заметно правее центра листа.
    c.check(f"p{p}_not_sheet_center",
            abs(cx - SHEET_CX) > 12,
            f"стр.{p}: cx={cx:.1f} подозрительно близко к центру ЛИСТА {SHEET_CX:.1f}")

    # Номер не уехал к краям полосы (не прижат влево/вправо).
    c.check(f"p{p}_not_at_edges",
            f[1] > LEFT + 50 and f[3] < RIGHT_EDGE - 50,
            f"стр.{p}: номер у края полосы x0={f[1]:.1f} x1={f[3]:.1f}")

c.done()
