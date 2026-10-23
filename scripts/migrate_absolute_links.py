#!/usr/bin/env python3
"""Rewrite file:// Markdown links to repository-relative links using explicit aliases."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping, Optional
from urllib.parse import unquote, urlparse
import argparse
import json
import os

try:
    from scripts.check_markdown_links import MARKDOWN_LINK_RE
except ModuleNotFoundError:  # 支持 `python3 scripts/migrate_absolute_links.py` 直接运行。
    from check_markdown_links import MARKDOWN_LINK_RE


def relative_project_path(absolute_path: Path, root: Path) -> Path | None:
    try:
        return absolute_path.relative_to(root)
    except ValueError:
        parts = absolute_path.parts
        for child in root.iterdir():
            if child.name in parts:
                return Path(*parts[parts.index(child.name) :])
    return None


def rewrite_document(
    source: Path,
    source_text: str,
    root: Path,
    aliases: Mapping[str, str],
    source_line_aliases: Optional[Mapping[str, str]] = None,
) -> tuple[str, int, list[str]]:
    root = root.resolve()
    source = source.resolve()
    changes = 0
    unresolved: list[str] = []
    source_relative = source.relative_to(root).as_posix()
    source_line_aliases = source_line_aliases or {}

    def replace(match):
        nonlocal changes
        target = match.group("target")
        if not target.startswith("file://"):
            return match.group(0)
        line = source_text.count("\n", 0, match.start()) + 1
        parsed = urlparse(target)
        absolute_path = Path(unquote(parsed.path))
        relative_path = relative_project_path(absolute_path, root)
        if relative_path is None:
            unresolved.append(target)
            return match.group(0)
        link_key = f"{relative_path.as_posix()}#{parsed.fragment}" if parsed.fragment else relative_path.as_posix()
        canonical_reference = source_line_aliases.get(
            f"{source_relative}:{line}",
            aliases.get(link_key, aliases.get(relative_path.as_posix(), relative_path.as_posix())),
        )
        canonical_path_text, separator, canonical_fragment = canonical_reference.partition("#")
        canonical = Path(canonical_path_text)
        if not (root / canonical).is_file():
            unresolved.append(target)
            return match.group(0)
        rendered = os.path.relpath(root / canonical, source.parent).replace(os.sep, "/")
        fragment = canonical_fragment if separator else parsed.fragment
        replacement = f"{rendered}{'#' + fragment if fragment else ''}"
        changes += 1
        return match.group(0).replace(target, replacement, 1)

    return MARKDOWN_LINK_RE.sub(replace, source_text), changes, unresolved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="仓库根目录")
    parser.add_argument(
        "--aliases",
        type=Path,
        default=Path("scripts/link-target-aliases.json"),
        help="旧路径到当前路径的 JSON 映射",
    )
    parser.add_argument("--apply", action="store_true", help="写回文件；默认仅预演")
    args = parser.parse_args()
    root = args.root.resolve()
    aliases_path = args.aliases if args.aliases.is_absolute() else root / args.aliases
    configuration = json.loads(aliases_path.read_text(encoding="utf-8"))
    if "path_aliases" in configuration:
        aliases = configuration["path_aliases"]
        source_line_aliases = configuration.get("source_line_aliases", {})
    else:
        aliases = configuration
        source_line_aliases = {}
    total_changes = 0
    unresolved: list[str] = []
    for document in sorted(root.rglob("*.md")):
        if ".git" in document.parts:
            continue
        original = document.read_text(encoding="utf-8")
        rewritten, changes, document_unresolved = rewrite_document(
            document, original, root, aliases, source_line_aliases
        )
        total_changes += changes
        unresolved.extend(document_unresolved)
        if args.apply and rewritten != original:
            document.write_text(rewritten, encoding="utf-8")
    print(f"{'已迁移' if args.apply else '预演'} {total_changes} 条绝对链接")
    if unresolved:
        print("未解析链接：")
        print("\n".join(sorted(set(unresolved))))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
