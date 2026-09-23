import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import book


class BookTests(unittest.TestCase):
    def test_duplicate_headings_have_distinct_links(self):
        tokens = book.PARSER.parse("# Пример\n\n## Типы и X/Z\n\n## Типы и X/Z\n")
        self.assertEqual([h[3] for h in book.headings(tokens)],
                         ["пример", "типы-и-xz", "типы-и-xz-1"])

    def test_external_and_relative_targets(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "docs/chapter.md"
            self.assertIsNone(book.local_target(source, "https://example.org/a#b", root))
            self.assertEqual(book.local_target(source, "../README.md#привет", root),
                             ((root / "README.md").resolve(), "привет"))
            self.assertEqual(book.local_target(source, "#раздел", root),
                             (source.resolve(), "раздел"))

    def test_escape_and_unsafe_scheme_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "chapter.md"
            for href in ("../outside.md", "javascript:alert(1)", "file:///etc/passwd"):
                with self.subTest(href=href), self.assertRaises(ValueError):
                    book.local_target(source, href, root)

    def test_manifest_and_all_repository_links(self):
        count, _ = book.check(allow_missing_artifacts=True)
        self.assertEqual(count, 39)

    def test_missing_fragment_is_detected(self):
        import json
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "docs").mkdir()
            (root / "book.json").write_text(json.dumps({"parts": [{
                "title": "Part", "chapters": [["1", "Title", "docs/chapter.md"]]
            }]}), encoding="utf-8")
            (root / "README.md").write_text(book.TOC_START + "\n" + book.TOC_END, encoding="utf-8")
            (root / "docs/chapter.md").write_text("# Title\n\n[bad](#absent)\n", encoding="utf-8")
            book.update_toc(root, write=True)
            with self.assertRaisesRegex(ValueError, "Missing anchor"):
                book.check(root)

    def test_merged_links_and_no_rewriting_in_code(self):
        meta, chapters = book.load_book()
        combined = book.merged_markdown(meta, chapters)
        self.assertIn('<a id="' + book.anchor_key(chapters[0].path) + '"></a>', combined)
        self.assertIn("assign sum = {1'b0, a} + {1'b0, b};", combined)
        self.assertNotIn("](../01-foundations/", combined)

    def test_published_fifo_matches_compiled_example(self):
        chapter = (book.ROOT / "docs/04-rtl/22-project.md").read_text(encoding="utf-8")
        example = (book.ROOT / "examples/rtl/sync_fifo.sv").read_text(encoding="utf-8")
        listings = [t.content for t in book.PARSER.parse(chapter) if t.type == "fence"]
        self.assertIn(example, listings)

    def test_published_fifo_testbench_matches_example(self):
        chapter = (book.ROOT / "docs/04-rtl/22-project.md").read_text(encoding="utf-8")
        example = (book.ROOT / "examples/tb/tb_fifo.sv").read_text(encoding="utf-8")
        listings = [t.content for t in book.PARSER.parse(chapter) if t.type == "fence"]
        self.assertIn(example, listings)


if __name__ == "__main__":
    unittest.main()
