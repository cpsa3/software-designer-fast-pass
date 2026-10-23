from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.migrate_absolute_links import rewrite_document


class AbsoluteLinkMigrationTests(unittest.TestCase):
    def test_rewrites_aliased_file_uri_to_relative_path(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "05-error-vault" / "cards.md"
            source.parent.mkdir()
            target = root / "01-fast-pass" / "14.面向对象技术速记指南.md"
            target.parent.mkdir()
            target.write_text("# 核心标题\n", encoding="utf-8")
            source_text = (
                f"[讲义](file://{root}/01-fast-pass/04.旧版讲义.md#核心标题)\n"
            )
            aliases = {
                "01-fast-pass/04.旧版讲义.md": "01-fast-pass/14.面向对象技术速记指南.md"
            }

            rewritten, changes, unresolved = rewrite_document(
                source, source_text, root, aliases
            )

            self.assertEqual(
                rewritten,
                "[讲义](../01-fast-pass/14.面向对象技术速记指南.md#核心标题)\n",
            )
            self.assertEqual(changes, 1)
            self.assertEqual(unresolved, [])

    def test_prefers_a_fragment_specific_alias(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "05-error-vault" / "cards.md"
            source.parent.mkdir()
            target = root / "01-fast-pass" / "06.安全性知识速记指南.md"
            target.parent.mkdir()
            target.write_text("# 防火墙\n", encoding="utf-8")
            source_text = (
                f"[安全题](file://{root}/01-fast-pass/04.网络与信息安全速记指南.md#防火墙)\n"
            )
            aliases = {
                "01-fast-pass/04.网络与信息安全速记指南.md": "01-fast-pass/05.计算机网络速记指南.md",
                "01-fast-pass/04.网络与信息安全速记指南.md#防火墙": "01-fast-pass/06.安全性知识速记指南.md#防火墙",
            }

            rewritten, changes, unresolved = rewrite_document(
                source, source_text, root, aliases
            )

            self.assertEqual(
                rewritten,
                "[安全题](../01-fast-pass/06.安全性知识速记指南.md#防火墙)\n",
            )
            self.assertEqual(changes, 1)
            self.assertEqual(unresolved, [])

    def test_prefers_source_line_alias_for_split_topics(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "05-error-vault" / "cards.md"
            source.parent.mkdir()
            target = root / "01-fast-pass" / "06.安全性知识速记指南.md"
            target.parent.mkdir()
            target.write_text("# 安全\n", encoding="utf-8")
            source_text = (
                "前置文本\n"
                f"[安全题](file://{root}/01-fast-pass/04.网络与信息安全速记指南.md)\n"
            )
            aliases = {
                "01-fast-pass/04.网络与信息安全速记指南.md": "01-fast-pass/05.计算机网络速记指南.md",
            }
            source_line_aliases = {
                "05-error-vault/cards.md:2": "01-fast-pass/06.安全性知识速记指南.md"
            }

            rewritten, changes, unresolved = rewrite_document(
                source, source_text, root, aliases, source_line_aliases
            )

            self.assertEqual(
                rewritten,
                "前置文本\n[安全题](../01-fast-pass/06.安全性知识速记指南.md)\n",
            )
            self.assertEqual(changes, 1)
            self.assertEqual(unresolved, [])


if __name__ == "__main__":
    unittest.main()
