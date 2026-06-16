"""pb paper-a4: размер листа ровно A4 (595.28 x 841.89 pt) по pdfinfo."""
import re
import subprocess

import helpers as h

c = h.Checks("pb_paper_a4_size")
pdf = h.compile("pb_paper_a4_size.typ")

info = subprocess.run([h.PDFINFO, pdf], capture_output=True, text=True).stdout
m = re.search(r"Page size:\s+([0-9.]+) x ([0-9.]+) pts", info)
w = float(m.group(1)) if m else None
ht = float(m.group(2)) if m else None

c.check("width_a4",
        w is not None and abs(w - 595.276) < 1,
        f"ширина листа {w} pt, ждём ~595.28 (A4)")

c.check("height_a4",
        ht is not None and abs(ht - 841.89) < 1,
        f"высота листа {ht} pt, ждём ~841.89 (A4)")

# pdfinfo сам помечает размер как (A4)
c.check("labelled_a4",
        "(A4)" in info,
        f"pdfinfo не распознал A4:\n{info}")

c.done()
