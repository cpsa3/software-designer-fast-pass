from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.normalize_markdown_anchors import rewrite_document


class MarkdownAnchorNormalizationTests(unittest.TestCase):
    def test_rewrites_only_to_a_known_normalized_anchor(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.md"
            target = root / "target.md"
            target.write_text("## 📌 中文 标题\n", encoding="utf-8")
            source_text = "[标题](target.md#📌-中文-标题)\n[未知](target.md#不存在)\n"

            rewritten, changes = rewrite_document(source, source_text, root)

            self.assertEqual(
                rewritten,
                "[标题](target.md#-中文-标题)\n[未知](target.md#不存在)\n",
            )
            self.assertEqual(changes, 1)


if __name__ == "__main__":
    unittest.main()
