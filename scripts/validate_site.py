#!/usr/bin/env python3
"""Validate the reviewable parts of the generated static site."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class GeneratedHTMLParser(HTMLParser):
    """Collect local links and basic accessibility errors from one HTML file."""

    def __init__(self, path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.path = path
        self.links: list[tuple[str, str, str]] = []
        self.errors: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id:
            if element_id in self.ids:
                self.errors.append(f"{self.path}: duplicate id {element_id!r}")
            self.ids.add(element_id)

        if tag.lower() == "img" and not (attributes.get("alt") or "").strip():
            self.errors.append(f"{self.path}: image is missing alt text")

        for attribute in ("href", "src"):
            value = attributes.get(attribute)
            if value:
                self.links.append((tag, attribute, value))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_files(root: Path) -> list[Path]:
    ignored_parts = {".git", ".bundle", "_site", "vendor", "node_modules"}
    return [
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".html", ".md", ".markdown", ".yml", ".yaml"}
        and not ignored_parts.intersection(path.parts)
    ]


def validate_source(root: Path) -> list[str]:
    errors: list[str] = []

    data_dir = root / "assets" / "data"
    for data_path in sorted(data_dir.glob("*.json")):
        try:
            json.loads(read_text(data_path))
        except json.JSONDecodeError as exc:
            errors.append(f"{data_path}: invalid JSON ({exc})")

    for path in source_files(root):
        text = read_text(path)

        include_pattern = (
            r"{%\s*include\s+(?:vega-lite|plotly)\.html\b"
            r"[^%]*\bspec\s*=\s*[\"']([^\"']+)[\"']"
        )
        for match in re.finditer(include_pattern, text):
            spec = match.group(1)
            parsed = urlsplit(spec)
            if parsed.scheme or parsed.netloc:
                continue
            spec_path = root / unquote(parsed.path).lstrip("/")
            if not spec_path.is_file():
                errors.append(f"{path}: referenced chart spec does not exist: {spec}")

        for match in re.finditer(
            r"<pre\b[^>]*class=[\"'][^\"']*\bmermaid\b[^\"']*[\"'][^>]*>(.*?)</pre>",
            text,
            flags=re.IGNORECASE | re.DOTALL,
        ):
            if not re.sub(r"\s+", "", match.group(1)):
                errors.append(f"{path}: Mermaid block is empty")

    return errors


def resolve_local_target(site: Path, page: Path, raw_url: str) -> Path | None:
    parsed = urlsplit(raw_url)
    if parsed.scheme or parsed.netloc:
        return None
    if parsed.path == "" or parsed.path == "/":
        target = site
    elif parsed.path.startswith("/"):
        target = site / unquote(parsed.path).lstrip("/")
    else:
        target = page.parent / unquote(parsed.path)

    try:
        target = target.resolve()
        target.relative_to(site.resolve())
    except ValueError:
        return None
    return target


def target_exists(site: Path, page: Path, raw_url: str) -> bool:
    target = resolve_local_target(site, page, raw_url)
    if target is None:
        return True
    if target.is_file():
        return True

    candidates = [target / "index.html"]
    if target.suffix == "":
        candidates.append(target.with_suffix(".html"))
    return any(candidate.is_file() for candidate in candidates)


def validate_generated_site(site: Path) -> list[str]:
    errors: list[str] = []
    if not site.is_dir():
        return [f"generated site directory does not exist: {site}"]
    if not (site / "index.html").is_file():
        errors.append(f"generated site is missing {site / 'index.html'}")

    html_files = sorted(site.rglob("*.html"))
    if not html_files:
        errors.append(f"generated site contains no HTML files: {site}")

    for path in html_files:
        parser = GeneratedHTMLParser(path)
        try:
            parser.feed(read_text(path))
            parser.close()
        except Exception as exc:  # HTMLParser errors should identify the file.
            errors.append(f"{path}: HTML parsing failed ({exc})")
            continue

        errors.extend(parser.errors)
        for tag, attribute, value in parser.links:
            if value.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
                continue
            if not target_exists(site, path, value):
                errors.append(f"{path}: missing local {attribute} target {value!r}")

    search_json = site / "search.json"
    if search_json.is_file():
        try:
            json.loads(read_text(search_json))
        except json.JSONDecodeError as exc:
            errors.append(f"{search_json}: invalid generated JSON ({exc})")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--site",
        type=Path,
        default=Path("_site"),
        help="generated Jekyll output directory (default: ./_site)",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    site = args.site if args.site.is_absolute() else (Path.cwd() / args.site)
    errors = validate_source(root)
    errors.extend(validate_generated_site(site.resolve()))

    if errors:
        print("Site validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    json_count = len(list((root / "assets" / "data").glob("*.json")))
    html_count = len(list(site.resolve().rglob("*.html")))
    print(f"Validated {json_count} JSON data file(s) and {html_count} generated HTML file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
