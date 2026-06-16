"""pl point 14: название модели 'L298N' не разрывается — целиком на одной
строке в узком box 40pt. 'яяя' переносится на строку выше."""
import helpers as h

c = h.Checks("pl_typo_model")
pdf = h.compile("pl_typo_model.typ")
ws = [w for w in h.words(pdf) if not (w[5].isdigit() and w[2] > 700)]

модель = next((w for w in ws if w[5] == "L298N"), None)
яяя = next((w for w in ws if w[5] == "яяя"), None)

c.check("model_intact", модель is not None,
        f"'L298N' распалась на токены: {[w[5] for w in ws]}")
c.check("no_fragments", not any(w[5] in ("L298N-", "L298", "N") for w in ws),
        f"есть осколки модели: {[w[5] for w in ws]}")
if модель and яяя:
    c.check("model_below_word", модель[2] > яяя[2] + 1.0,
            f"перенос не сработал: yMin яяя={яяя[2]:.1f} L298N={модель[2]:.1f}")
else:
    c.check("model_below_word", False, "нет слов для проверки")
c.done()
