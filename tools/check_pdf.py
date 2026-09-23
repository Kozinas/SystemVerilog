"""Verify generated PDF structure, extractable Cyrillic, links and code markers."""
from pathlib import Path
import sys
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from book import load_book


def main():
    reader = PdfReader(ROOT / "dist/systemverilog.pdf")
    meta, chapters = load_book()
    texts = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(texts)
    errors = []
    for chapter in chapters:
        # Titles can wrap; normalize whitespace before comparison.
        if " ".join(chapter.title.split()) not in " ".join(text.split()):
            errors.append("Missing chapter title: " + chapter.title)
    if "�" in text:
        errors.append("Replacement character in extracted PDF text")
    for marker in ("always_ff", "SystemVerilog", "Упражнение 01", "Упражнение 33", "Оглавление"):
        if marker not in text:
            errors.append("Missing text marker: " + marker)
    internal, external = 0, 0
    for page in reader.pages:
        for ref in page.get("/Annots", []):
            annot = ref.get_object()
            action = annot.get("/A", {})
            if "/Dest" in annot or action.get("/S") == "/GoTo": internal += 1
            if action.get("/S") == "/URI": external += 1
    if internal < len(chapters): errors.append("Too few internal PDF links")
    if external == 0: errors.append("Missing external source links")
    if not reader.outline: errors.append("Missing PDF bookmarks")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS PDF: {len(reader.pages)} pages, {len(chapters)} chapter titles, "
          f"{internal} internal links, {external} external links, Cyrillic text and bookmarks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
