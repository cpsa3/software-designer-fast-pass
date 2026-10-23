#!/usr/bin/env python3
"""Normalize local Markdown anchor fragments only when the target anchor exists."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote
import argparse

try:
    from scripts.check_markdown_links import (
        EXTERNAL_SCHEMES,
        MARKDOWN_LINK_RE,
        anchors_in,
        is_within,
        slugify_heading,
    )
except ModuleNotFoundError:  # 支持 `python3 scripts/normalize_markdown_anchors.py` 直接运行。
    from check_markdown_links import (
        EXTERNAL_SCHEMES,
        MARKDOWN_LINK_RE,
        anchors_in,
        is_within,
        slugify_heading,
    )


def rewrite_document(source: Path, source_text: str, root: Path) -> tuple[str, int]:
    root = root.resolve()
    source = source.resolve()
    cache: dict[Path, set[str]] = {}
    changes = 0

    def replace(match):
        nonlocal changes
        target = unquote(match.group("target"))
        if target.startswith(("file://", "/", *EXTERNAL_SCHEMES)):
            return match.group(0)
        path_part, separator, fragment = target.partition("#")
        if not separator or not fragment:
            return match.group(0)
        target_document = source if not path_part else (source.parent / path_part).resolve()
        if not is_within(target_document, root) or not target_document.is_file():
            return match.group(0)
        known_anchors = cache.setdefault(target_document, anchors_in(target_document))
        if fragment in known_anchors:
            return match.group(0)
        normalized = slugify_heading(fragment)
        if normalized not in known_anchors:
            return match.group(0)
        changes += 1
        replacement = f"{path_part}#{normalized}"
        return match.group(0).replace(match.group("target"), replacement, 1)

    return MARKDOWN_LINK_RE.sub(replace, source_text), changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="仓库根目录")
    parser.add_argument("--apply", action="store_true", help="写回文件；默认仅预演")
    args = parser.parse_args()
    root = args.root.resolve()
    total_changes = 0
    for document in sorted(root.rglob("*.md")):
        if ".git" in document.parts:
            continue
        original = document.read_text(encoding="utf-8")
        rewritten, changes = rewrite_document(document, original, root)
        total_changes += changes
        if args.apply and rewritten != original:
            document.write_text(rewritten, encoding="utf-8")
    print(f"{'已规范化' if args.apply else '预演'} {total_changes} 个标题锚点")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
