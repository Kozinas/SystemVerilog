"""Compile independent example groups with slang; this does not simulate."""
from pathlib import Path
import json
import re
import sys

import pyslang

ROOT = Path(__file__).resolve().parents[1]
GROUPS = [
    ("fifo", "1800-2017", ["rtl/sync_fifo.sv", "tb/tb_fifo.sv"]),
    ("core", "1800-2017", ["language/core.sv"]),
    ("verification", "1800-2017", ["language/verification.sv"]),
    ("primitives", "1800-2017", ["language/primitives.sv"]),
    ("sv2023", "1800-2023", ["language/sv2023.sv"]),
]


def main():
    results = []
    reference = (ROOT / "docs/appendices/b-reference.md").read_text(encoding="utf-8")
    words = re.search(r"```text\n(.*?)```", reference, re.S).group(1).split()
    listed = {word.replace("_", "") for word in words}
    expected = {name[:-7].lower() for name in dir(pyslang.parsing.TokenKind)
                if name.endswith("Keyword")}
    keywords_ok = listed == expected and len(words) == len(set(words))
    print(f"{'PASS' if keywords_ok else 'FAIL'} keyword reference: {len(words)} words")
    if not keywords_ok:
        print(f"Missing: {sorted(expected - listed)}; unexpected: {sorted(listed - expected)}")
    for name, standard, paths in GROUPS:
        driver = pyslang.driver.Driver()
        driver.addStandardArgs()
        driver.setTerminalColorsEnabled(False)
        filenames = " ".join('"' + (ROOT / "examples" / p).as_posix() + '"' for p in paths)
        ok = driver.parseCommandLine(f"slang --std {standard} {filenames}")
        ok = ok and driver.processOptions() and driver.parseAllSources()
        if ok:
            compilation = driver.createCompilation()
            driver.reportCompilation(compilation, False)
            ok = driver.reportDiagnostics(False)
        results.append({"group": name, "standard": standard, "passed": bool(ok)})
        print(f"{'PASS' if ok else 'FAIL'} compile {name}", flush=True)
    output = ROOT / "build"
    output.mkdir(exist_ok=True)
    (output / "sv-check.json").write_text(json.dumps({
        "tool": "pyslang", "version": pyslang.__version__,
        "kind": "compilation, not simulation", "results": results,
        "keyword_reference_passed": keywords_ok,
    }, indent=2) + "\n", encoding="utf-8")
    return 0 if keywords_ok and all(r["passed"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
