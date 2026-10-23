from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.check_markdown_links import scan_repository


class MarkdownLinkCheckTests(unittest.TestCase):
    def write(self, root: Path, relative: str, content: str) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_reports_machine_specific_file_uri(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "notes.md", "[本机文件](file:///Users/example/notes.md)\n")

            issues = scan_repository(root)

            self.assertEqual([issue.code for issue in issues], ["absolute_path"])

    def test_reports_missing_file_and_anchor(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "target.md", "# 已存在标题\n")
            self.write(
                root,
                "source.md",
                "[缺文件](missing.md)\n[缺锚点](target.md#不存在标题)\n",
            )

            issues = scan_repository(root)

            self.assertEqual(
                [issue.code for issue in issues],
                ["missing_file", "missing_anchor"],
            )

    def test_accepts_relative_gfm_and_explicit_anchors(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(
                root,
                "target.md",
                "# 📌 中文 标题\n<a id=\"custom-anchor\"></a>\n",
            )
            self.write(
                root,
                "source.md",
                "[标题](target.md#-中文-标题)\n[显式锚点](target.md#custom-anchor)\n",
            )

            self.assertEqual(scan_repository(root), [])

    def test_accepts_repository_directory_links(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "guides").mkdir()
            self.write(root, "source.md", "[目录](guides/)\n")

            self.assertEqual(scan_repository(root), [])


if __name__ == "__main__":
    unittest.main()
