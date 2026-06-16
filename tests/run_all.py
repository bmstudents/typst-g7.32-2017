#!/usr/bin/env python3
"""Раннер тест-харнесса: запускает все tests/*.py (кроме служебных),
собирает PASS/FAIL по каждому файлу и общий итог."""
import glob
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKIP = {"helpers.py", "run_all.py"}


def _run(f):
    r = subprocess.run([sys.executable, f], capture_output=True, text=True)
    return f, r.returncode, r.stdout + r.stderr


def main():
    files = sorted(f for f in glob.glob(os.path.join(TESTS_DIR, "*.py"))
                   if os.path.basename(f) not in SKIP)
    suites_ok = suites_fail = 0
    checks_ok = checks_fail = 0
    failed = []
    # typst-компиляция через sshfs медленная — гоняем тесты параллельно
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(_run, files))
    for f, code, out in results:
        for line in out.splitlines():
            if line.startswith("PASS "):
                checks_ok += 1
            elif line.startswith("FAIL "):
                checks_fail += 1
        print(out.rstrip())
        if code == 0:
            suites_ok += 1
        else:
            suites_fail += 1
            failed.append(os.path.basename(f))
    print("=" * 60)
    print(f"ФАЙЛОВ: {suites_ok} ok / {suites_fail} fail   "
          f"ПРОВЕРОК: {checks_ok} ok / {checks_fail} fail")
    if failed:
        print("упали:", ", ".join(failed))
    sys.exit(1 if suites_fail else 0)


if __name__ == "__main__":
    main()
