#!/usr/bin/env python3
"""
Lightweight ISA spec linter for spec prose (Markdown/AsciiDoc/plain text).

Checks for:
- TODO/TBD markers accidentally left in normative text
- "weasel words" that usually hide ambiguity
- lowercase RFC-2119 terms (prefer uppercase MUST/SHOULD/MAY)

This is intentionally conservative: it reports warnings for review rather than
trying to "auto-fix" a spec.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


WEASEL_WORDS = [
    "usually",
    "typically",
    "often",
    "sometimes",
    "some",
    "many",
    "few",
    "fast",
    "small",
    "simple",
    "as needed",
    "etc",
]

RFC2119_TERMS = ["must", "must not", "shall", "shall not", "should", "should not", "may"]


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    col: int
    kind: str
    message: str

    def format(self) -> str:
        return f"{self.path}:{self.line}:{self.col}: {self.kind}: {self.message}"


def _iter_findings_for_line(path: Path, line_no: int, line: str) -> list[Finding]:
    findings: list[Finding] = []

    def add(kind: str, match: re.Match[str], message: str) -> None:
        findings.append(
            Finding(
                path=path,
                line=line_no,
                col=match.start() + 1,
                kind=kind,
                message=message,
            )
        )

    for marker in ("TODO", "TBD"):
        for m in re.finditer(rf"\b{marker}\b", line):
            add("marker", m, f"Found '{marker}' (remove or make non-normative).")

    for word in WEASEL_WORDS:
        for m in re.finditer(rf"(?i)\b{re.escape(word)}\b", line):
            add("weasel", m, f"Ambiguous term '{m.group(0)}' (rewrite precisely).")

    # RFC-2119 terms: allow uppercase, flag lowercase/mixed-case.
    for term in RFC2119_TERMS:
        pattern = rf"\b{re.escape(term)}\b"
        for m in re.finditer(pattern, line, flags=re.IGNORECASE):
            text = m.group(0)
            if text.upper() == text:
                continue
            add("rfc2119", m, f"Use uppercase RFC-2119 term '{text.upper()}'.")

    return findings


def lint_file(path: Path) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")

    findings: list[Finding] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        findings.extend(_iter_findings_for_line(path, idx, line))
    return findings


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Lint ISA spec text for ambiguity.")
    p.add_argument("paths", nargs="+", help="Markdown/text files or directories to lint.")
    p.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any findings are reported.",
    )
    return p.parse_args(argv)


def expand_paths(raw_paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for raw in raw_paths:
        path = Path(raw)
        if path.is_dir():
            out.extend(
                sorted(
                    p
                    for p in path.rglob("*")
                    if p.is_file() and p.suffix in {".md", ".txt", ".adoc", ".asciidoc"}
                )
            )
        else:
            out.append(path)
    return out


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    paths = expand_paths(args.paths)

    all_findings: list[Finding] = []
    for path in paths:
        if not path.exists():
            print(f"{path}:0:0: error: file not found", file=sys.stderr)
            return 2
        all_findings.extend(lint_file(path))

    if all_findings:
        for f in all_findings:
            print(f.format())
        return 1 if args.strict else 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
