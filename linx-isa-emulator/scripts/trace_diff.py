#!/usr/bin/env python3
"""
Compare two trace logs and point at the first divergence.

This is a simple helper for difftest bring-up. It treats each non-empty line as
one record and compares them after optional normalization.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def _read_lines(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    return [line.rstrip("\n") for line in text.splitlines()]


def _normalize(line: str, ignore_regexes: list[re.Pattern[str]]) -> str:
    out = line.strip()
    for rx in ignore_regexes:
        out = rx.sub("", out)
    out = re.sub(r"\s+", " ", out).strip()
    return out


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Diff two trace logs (first mismatch).")
    p.add_argument("golden", help="Reference trace log")
    p.add_argument("candidate", help="Trace log under test")
    p.add_argument(
        "--ignore",
        action="append",
        default=[],
        help="Regex to remove before comparison (repeatable).",
    )
    p.add_argument(
        "--context",
        type=int,
        default=2,
        help="Lines of context to show around the mismatch.",
    )
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    golden_path = Path(args.golden)
    cand_path = Path(args.candidate)
    if not golden_path.exists() or not cand_path.exists():
        print("error: input file(s) not found", file=sys.stderr)
        return 2

    ignore_regexes = [re.compile(pat) for pat in args.ignore]
    golden = [_normalize(l, ignore_regexes) for l in _read_lines(golden_path) if l.strip()]
    cand = [_normalize(l, ignore_regexes) for l in _read_lines(cand_path) if l.strip()]

    limit = max(len(golden), len(cand))
    for i in range(limit):
        g = golden[i] if i < len(golden) else None
        c = cand[i] if i < len(cand) else None
        if g != c:
            lo = max(0, i - args.context)
            hi = i + args.context + 1
            print(f"mismatch at record {i} (0-based):")
            print("--- golden ---")
            for j in range(lo, min(hi, len(golden))):
                prefix = ">>" if j == i else "  "
                print(f"{prefix} {j}: {golden[j]}")
            print("--- candidate ---")
            for j in range(lo, min(hi, len(cand))):
                prefix = ">>" if j == i else "  "
                print(f"{prefix} {j}: {cand[j]}")
            if g is None:
                print("note: golden ended early")
            if c is None:
                print("note: candidate ended early")
            return 1

    print("ok: traces match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
