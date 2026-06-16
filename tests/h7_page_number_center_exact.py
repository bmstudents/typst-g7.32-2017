"""h7_page_number_center_exact: номер страницы стоит ПО ЦЕНТРУ нижнего поля.

Жёстко (координаты, не «номер есть»):
  - горизонтальный центр глифа номера cx ∈ [316, 322] (центр текст. поля 318.9pt
    = (85.04+552.76)/2). Узкий коридор ±~3pt вокруг точного центра.
  - номер лежит в НИЖНЕМ поле листа: yMin > 780 (лист A4 = 841.89pt, нижнее
    поле начинается ~786pt). Проверяем, что это именно футер, а не контент.
  - номера растут постранично (2,3,4) и совпадают с номером физической страницы.
Проверяем на нескольких страницах — центр должен быть стабилен.
"""
import helpers as h

c = h.Checks("h7_page_number_center_exact")
pdf = h.compile("h7_page_number_center_exact.typ")

c.check("four_pages", h.page_count(pdf) == 4, f"страниц {h.page_count(pdf)}, ждём 4")

# Для каждой страницы 2..4 находим её номер как самое нижнее слово-цифру.
centers = []
ymins = []
ok_values = True
for page in (2, 3, 4):
    nums = [w for w in h.words(pdf) if w[0] == page and w[5].isdigit() and w[2] > 700]
    if not nums:
        c.check(f"num_present_p{page}", False, f"нет номера-футера на стр {page}")
        ok_values = False
        continue
    foot = max(nums, key=lambda t: t[2])
    cx = (foot[1] + foot[3]) / 2
    centers.append((page, cx, foot))
    ymins.append(foot[2])  # yMin номера
    if foot[5] != str(page):
        ok_values = False

# Значения номеров = номерам страниц.
c.check("numbers_match_pages", ok_values and len(centers) == 3,
        f"номера не совпали со страницами: {[(p, f[5]) for p, _, f in centers]}")

# Горизонтальный центр в узком коридоре [316, 322] на КАЖДОЙ странице.
center_ok = all(316.0 <= cx <= 322.0 for _, cx, _ in centers)
c.check("center_in_band_316_322", center_ok,
        f"центры номеров вне [316,322]: {[(p, round(cx, 2)) for p, cx, _ in centers]}")

# Низ страницы: yMin номера > 780 (в нижнем поле).
bottom_ok = all(y > 780 for y in ymins) and len(ymins) == 3
c.check("number_in_bottom_margin", bottom_ok,
        f"номер не в нижнем поле: yMin={[round(y, 1) for y in ymins]}, ждём >780")

c.done()
