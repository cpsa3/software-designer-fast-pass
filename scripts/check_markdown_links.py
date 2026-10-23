#!/usr/bin/env python3
"""Validate repository-local Markdown links and anchors."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote
import argparse
import re
import unicodedata


MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\((?P<target>[^\s)]+)(?:\s+[^)]*)?\)")
EXPLICIT_ANCHOR_RE = re.compile(
    r"<a\b[^>]*\bid\s*=\s*[\"'](?P<id>[^\"']+)[\"'][^>]*>", re.IGNORECASE
)
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(?P<text>.*?)(?:\s+#+)?\s*$")
EXTERNAL_SCHEMES = ("http://", "https://", "mailto:", "tel:")


@dataclass(frozen=True)
class Issue:
    code: str
    source: Path
    line: int
    target: str
    detail: str


def slugify_heading(raw_heading: str) -> str:
    """Mirror the heading slug rules used by the repository profile generator."""
    cleaned = []
    for character in raw_heading.strip().lower():
        category = unicodedata.category(character)
        if "\u2460" <= character <= "\u24ff":
            continue
        if (
            character in ("-", "_")
            or character.isalnum()
            or character.isspace()
            or not category.startswith(("P", "S", "C"))
        ):
            cleaned.append(character)
    return re.sub(r"\s", "-", "".join(cleaned))


def anchors_in(document: Path) -> set[str]:
    text = document.read_text(encoding="utf-8")
    anchors = {match.group("id") for match in EXPLICIT_ANCHOR_RE.finditer(text)}
    occurrences: dict[str, int] = {}
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue
        base = slugify_heading(match.group("text"))
        count = occurrences.get(base, 0)
        occurrences[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def issue_path(root: Path, path: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def scan_document(document: Path, root: Path, anchors: dict[Path, set[str]]) -> list[Issue]:
    text = document.read_text(encoding="utf-8")
    issues: list[Issue] = []
    for match in MARKDOWN_LINK_RE.finditer(text):
        target = unquote(match.group("target"))
        line = text.count("\n", 0, match.start()) + 1
        source = issue_path(root, document)
        if target.startswith("file://") or target.startswith("/"):
            issues.append(Issue("absolute_path", source, line, target, "本机绝对路径"))
            continue
        if target.startswith(EXTERNAL_SCHEMES):
            continue

        path_part, separator, fragment = target.partition("#")
        target_document = document if not path_part else (document.parent / path_part).resolve()
        if not is_within(target_document, root):
            issues.append(Issue("outside_repository", source, line, target, "目标位于仓库外"))
            continue
        if not target_document.exists():
            issues.append(Issue("missing_file", source, line, target, "目标文件不存在"))
            continue
        if separator and fragment and target_document.is_file():
            target_anchors = anchors.setdefault(target_document, anchors_in(target_document))
            if fragment not in target_anchors:
                issues.append(Issue("missing_anchor", source, line, target, "标题或显式锚点不存在"))
    return issues


def scan_repository(root: Path) -> list[Issue]:
    root = root.resolve()
    anchors: dict[Path, set[str]] = {}
    issues: list[Issue] = []
    for document in sorted(root.rglob("*.md")):
        if ".git" in document.parts:
            continue
        issues.extend(scan_document(document.resolve(), root, anchors))
    return issues


def format_issues(issues: Iterable[Issue]) -> str:
    return "\n".join(
        f"{issue.source}:{issue.line}: {issue.code}: {issue.target} ({issue.detail})"
        for issue in issues
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="仓库根目录")
    args = parser.parse_args()
    issues = scan_repository(args.root)
    if issues:
        print(format_issues(issues))
        print(f"链接检查失败：{len(issues)} 项问题")
        return 1
    print("链接检查通过：未发现本地 Markdown 链接问题")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
