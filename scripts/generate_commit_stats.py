#!/usr/bin/env python3
"""Generate a MonoMarket Conventional Commit breakdown as an SVG.

Only non-merge commits whose subjects begin with a recognized Conventional
Commit type are counted. Scoped commits and breaking-change markers are
supported; all other commit subjects are intentionally excluded.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from collections import Counter
from pathlib import Path
from xml.sax.saxutils import escape


TYPES = ("feat", "fix", "test", "refactor", "chore", "ci", "docs", "build")
SUBJECT_PATTERN = re.compile(
    r"^(feat|fix|test|refactor|chore|ci|docs|build)(?:\([^\r\n)]*\))?!?:\s+",
    re.IGNORECASE,
)


def get_subjects(repository: Path) -> list[str]:
    git_executable = os.environ.get("GIT_EXECUTABLE", "git")
    result = subprocess.run(
        [
            git_executable,
            "-c",
            f"safe.directory={repository.resolve().as_posix()}",
            "-C",
            str(repository),
            "log",
            "--no-merges",
            "--format=%s",
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.splitlines()


def classify(subjects: list[str]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for subject in subjects:
        match = SUBJECT_PATTERN.match(subject)
        if match:
            counts[match.group(1).lower()] += 1
    return counts


def render_svg(counts: Counter[str]) -> str:
    rows = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    total = sum(counts.values())
    width = 760
    left = 114
    chart_width = 410
    row_height = 35
    height = 96 + max(1, len(rows)) * row_height + 34
    maximum = max(counts.values(), default=1)
    svg_rows: list[str] = []

    for index, (commit_type, count) in enumerate(rows):
        y = 72 + index * row_height
        bar_width = round(chart_width * count / maximum)
        percentage = count * 100 / total
        svg_rows.append(
            f'<text class="label" x="{left - 14}" y="{y + 15}" text-anchor="end">{escape(commit_type)}</text>'
            f'<rect class="track" x="{left}" y="{y + 3}" width="{chart_width}" height="16" rx="4" />'
            f'<rect class="bar" x="{left}" y="{y + 3}" width="{bar_width}" height="16" rx="4" />'
            f'<text class="value" x="{left + chart_width + 14}" y="{y + 15}">{count} · {percentage:.1f}%</text>'
        )

    empty = ""
    if not rows:
        empty = '<text class="value" x="380" y="108" text-anchor="middle">No recognized Conventional Commit subjects found.</text>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">
  <title id="title">MonoMarket commit breakdown</title>
  <desc id="description">Distribution of recognized Conventional Commit types in non-merge MonoMarket commits.</desc>
  <style>
    .title {{ fill: #24292f; font: 600 18px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    .meta {{ fill: #57606a; font: 13px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    .label {{ fill: #24292f; font: 600 13px ui-monospace, SFMono-Regular, Menlo, monospace; }}
    .value {{ fill: #57606a; font: 13px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    .track {{ fill: #d0d7de; opacity: .55; }}
    .bar {{ fill: #0969da; }}
    @media (prefers-color-scheme: dark) {{
      .title, .label {{ fill: #f0f6fc; }}
      .meta, .value {{ fill: #8b949e; }}
      .track {{ fill: #30363d; }}
      .bar {{ fill: #58a6ff; }}
    }}
  </style>
  <a href="https://github.com/myngh04/monomarket">
    <text class="title" x="24" y="32">MonoMarket · Commit Breakdown</text>
    <text class="meta" x="24" y="53">{total} classified non-merge commits</text>
    {''.join(svg_rows)}
    {empty}
  </a>
</svg>
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    svg = render_svg(classify(get_subjects(args.repository)))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
