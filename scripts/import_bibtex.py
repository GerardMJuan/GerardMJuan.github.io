#!/usr/bin/env python3
"""Convert a BibTeX export into _data/publications.yml.

Google Scholar has no usable public API and blocks scripted access, so the
supported path is a manual export:

    1. Open your Scholar profile, tick the papers you want (or the header
       checkbox for all of them).
    2. Export -> BibTeX, and save the file as citations.bib.
    3. python3 scripts/import_bibtex.py citations.bib > _data/publications.yml

BibTeX carries no topic, so every entry comes out with `topic: uncategorised`.
Assign real topics afterwards and keep the `topics:` map at the top in sync —
that field is what colours the timeline chart.

Existing topic assignments are preserved: pass the current data file with
--merge and any entry whose title already appears there keeps its topic.

    python3 scripts/import_bibtex.py citations.bib --merge _data/publications.yml
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Types Scholar emits, mapped to the two the site's template understands.
TYPE_MAP = {
    "article": "journal",
    "inproceedings": "conference",
    "conference": "conference",
    "incollection": "conference",
    "proceedings": "conference",
    "book": "book",
    "phdthesis": "thesis",
    "mastersthesis": "thesis",
    "techreport": "preprint",
    "misc": "preprint",
    "unpublished": "preprint",
}

LATEX_ACCENTS = {
    # Dotless forms first — Scholar writes í as {\'\i}, so \'\i must be
    # replaced before the bare \i collapses to a plain i.
    r"\'\i": "í", r"\`\i": "ì", r"\^\i": "î", r"\"\i": "ï", r"\i": "i",
    r"\'a": "á", r"\'e": "é", r"\'i": "í", r"\'o": "ó", r"\'u": "ú",
    r"\'A": "Á", r"\'E": "É", r"\'I": "Í", r"\'O": "Ó", r"\'U": "Ú",
    r"\`a": "à", r"\`e": "è", r"\`i": "ì", r"\`o": "ò", r"\`u": "ù",
    r"\"a": "ä", r"\"e": "ë", r"\"i": "ï", r"\"o": "ö", r"\"u": "ü",
    r"\~n": "ñ", r"\~N": "Ñ", r"\c c": "ç", r"\c C": "Ç",
    r"\^a": "â", r"\^e": "ê", r"\^i": "î", r"\^o": "ô", r"\^u": "û",
    r"\ss": "ß", r"\&": "&", r"\%": "%", r"\_": "_", r"\$": "$",
    "--": "–",
}


def clean(value: str) -> str:
    """Undo the LaTeX-isms Scholar exports, and collapse whitespace."""
    value = value.strip().strip(",").strip()

    # {Protected Capitals} -> Protected Capitals, innermost braces first.
    for _ in range(6):
        new = re.sub(r"\{([^{}]*)\}", r"\1", value)
        if new == value:
            break
        value = new

    for latex, char in LATEX_ACCENTS.items():
        value = value.replace(latex, char)

    return re.sub(r"\s+", " ", value).strip()


def format_authors(raw: str) -> str:
    """'Last, First and Other, Name' -> 'Last, F., Other, N.'"""
    people = []
    for person in re.split(r"\s+and\s+", raw):
        person = person.strip()
        if not person:
            continue

        if "," in person:
            last, _, first = person.partition(",")
        else:
            parts = person.rsplit(" ", 1)
            last, first = (parts[1], parts[0]) if len(parts) == 2 else (person, "")

        initials = " ".join(
            f"{token[0]}." for token in first.replace(".", " ").split() if token
        )
        people.append(f"{last.strip()}, {initials}".strip().rstrip(","))

    return ", ".join(people)


def parse_bibtex(text: str) -> list[dict]:
    """Pull each @entry{...} apart into a field dict."""
    entries = []

    for match in re.finditer(r"@(\w+)\s*\{([^,]*),", text):
        kind = match.group(1).lower()

        # Walk from the opening brace to its match, so nested braces survive.
        start = text.index("{", match.start())
        depth, end = 0, len(text)
        for index in range(start, len(text)):
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
                if depth == 0:
                    end = index
                    break

        body = text[start + 1 : end]
        fields = {"__type__": kind}
        fields.update(parse_fields(body))

        entries.append(fields)

    return entries


def parse_fields(body: str) -> dict[str, str]:
    """Split an entry body into key = value pairs.

    Hand-rolled rather than a regex because BibTeX values nest braces —
    {MC-RVAE: ... {A}lzheimer's ...} — and a non-greedy regex stops at the
    first inner closing brace, silently truncating titles and author lists.
    """
    fields: dict[str, str] = {}
    index, length = 0, len(body)

    while index < length:
        key_match = re.compile(r"(\w+)\s*=\s*").match(body, index)
        if not key_match:
            index += 1
            continue

        key = key_match.group(1).lower()
        index = key_match.end()
        if index >= length:
            break

        if body[index] == "{":
            depth, start = 0, index
            while index < length:
                if body[index] == "{":
                    depth += 1
                elif body[index] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                index += 1
            value = body[start + 1 : index]
            index += 1
        elif body[index] == '"':
            index += 1
            start = index
            while index < length and body[index] != '"':
                index += 1
            value = body[start:index]
            index += 1
        else:
            start = index
            while index < length and body[index] != ",":
                index += 1
            value = body[start:index]

        fields[key] = value

        # Skip past the separating comma.
        while index < length and body[index] in ", \t\r\n":
            index += 1

    return fields


def to_record(fields: dict) -> dict | None:
    title = clean(fields.get("title", ""))
    if not title:
        return None

    venue = clean(
        fields.get("journal")
        or fields.get("booktitle")
        or fields.get("publisher")
        or fields.get("school")
        or ""
    )

    bits = []
    if fields.get("volume"):
        volume = clean(fields["volume"])
        bits.append(
            f"{volume}({clean(fields['number'])})" if fields.get("number") else volume
        )
    if fields.get("pages"):
        bits.append(clean(fields["pages"]))

    year = clean(fields.get("year", ""))

    return {
        "title": title,
        "authors": format_authors(clean(fields.get("author", ""))),
        "venue": venue,
        "details": ", ".join(bits),
        "year": int(year) if year.isdigit() else 0,
        "type": TYPE_MAP.get(fields["__type__"], "preprint"),
        "topic": "uncategorised",
        "doi": clean(fields.get("doi", "")),
        "url": clean(fields.get("url", "")),
    }


def quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def existing_topics(path: Path) -> dict[str, str]:
    """Scrape title -> topic out of the current YAML, so edits survive a re-import.

    Deliberately a regex rather than a YAML parse: this script runs in a bare
    GitHub Pages checkout, where PyYAML is not guaranteed to be installed.
    """
    if not path.exists():
        return {}

    topics, title = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        found = re.match(r'\s*-?\s*title:\s*"?(.*?)"?\s*$', line)
        if found:
            title = found.group(1)
            continue
        found = re.match(r"\s*topic:\s*(\S+)\s*$", line)
        if found and title:
            topics[title] = found.group(1)
            title = None

    return topics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bibtex", type=Path, help="BibTeX file exported from Scholar")
    parser.add_argument(
        "--merge",
        type=Path,
        metavar="YAML",
        help="existing publications.yml to carry topic assignments over from",
    )
    args = parser.parse_args()

    if not args.bibtex.exists():
        print(f"error: {args.bibtex} not found", file=sys.stderr)
        return 1

    known = existing_topics(args.merge) if args.merge else {}

    records = [r for r in (to_record(f) for f in parse_bibtex(
        args.bibtex.read_text(encoding="utf-8"))) if r]
    records.sort(key=lambda r: (-r["year"], r["title"]))

    if not records:
        print("error: no entries parsed — is this a BibTeX file?", file=sys.stderr)
        return 1

    for record in records:
        if record["title"] in known:
            record["topic"] = known[record["title"]]

    out = [
        "# Publications — generated by scripts/import_bibtex.py.",
        "# Re-run with --merge to keep the topic assignments below.",
        "",
        "self_names:",
        '  - "Martí-Juan, G."',
        '  - "Martí, G."',
        "",
        "# Add a label for every topic used below; these colour the timeline chart.",
        "topics:",
        "  uncategorised: \"Uncategorised\"",
        "",
        "entries:",
    ]

    for record in records:
        out.append(f"  - title: {quote(record['title'])}")
        out.append(f"    authors: {quote(record['authors'])}")
        if record["venue"]:
            out.append(f"    venue: {quote(record['venue'])}")
        if record["details"]:
            out.append(f"    details: {quote(record['details'])}")
        out.append(f"    year: {record['year']}")
        out.append(f"    type: {record['type']}")
        out.append(f"    topic: {record['topic']}")
        if record["doi"]:
            out.append(f"    doi: {quote(record['doi'])}")
        elif record["url"]:
            out.append(f"    url: {quote(record['url'])}")
        out.append("")

    print("\n".join(out).rstrip() + "\n")
    print(
        f"Wrote {len(records)} entries. Set the `topic:` fields and the `topics:` map.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
