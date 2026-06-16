"""pl point 14 (вариант с внутренним дефисом): пакет обещает, что модель
'ESP32-S2' не рвётся ВНУТРИ по дефису. Box 56pt позволяет модели целиком
встать на отдельную строку (она ~55pt), 'яяя' уходит выше.

ОЖИДАНИЕ: модель одним токеном на одной строке. Фича заменяет литеральный
дефис на неразрывный U+2011 (box() сам по себе разрыв по '-' не подавляет),
поэтому сравниваем, нормализуя дефис: и 'ESP32-S2', и 'ESP32‑S2' валидны —
важно, что НЕ разбита на 'ESP32-' / 'S2'."""
import helpers as h


def norm(s):
    return s.replace("‑", "-")


c = h.Checks("pl_typo_model_hyphen")
pdf = h.compile("pl_typo_model_hyphen.typ")
ws = [w for w in h.words(pdf) if not (w[5].isdigit() and w[2] > 700)]

whole = next((w for w in ws if norm(w[5]) == "ESP32-S2"), None)
frag = any(norm(w[5]) in ("ESP32-", "ESP32") for w in ws) and any(w[5] == "S2" for w in ws)

c.check("model_not_split_by_inner_hyphen", whole is not None and not frag,
        f"модель разорвана по внутреннему дефису (баг неразрывности): "
        f"токены={[w[5] for w in ws]}")
c.done()
