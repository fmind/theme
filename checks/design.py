"""Lint DESIGN.md and verify generated CSS and Tailwind token files stay in sync."""

import difflib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "DESIGN.md"
EXPORTS: tuple[tuple[tuple[str, ...], Path], ...] = (
    (("--format", "css-vars", "--prefix", "fmind"), ROOT / "themes/css/fmind.css"),
    (("--format", "css-tailwind"), ROOT / "themes/tailwind/fmind.css"),
)


def run_design_md(*args: str, timeout: int = 30) -> str:
    """Run design.md with bounded timeout, closed stdin, and UTF-8 decoding."""
    result = subprocess.run(
        ["design.md", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        stdin=subprocess.DEVNULL,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        detail = "\n".join(part for part in (result.stderr.strip(), result.stdout.strip()) if part)
        raise RuntimeError(f"design.md {' '.join(args)} failed (exit {result.returncode}): {detail}")
    return result.stdout


def main() -> int:
    """Lint DESIGN.md (failing on warnings/errors) and verify generated token files."""
    findings = [f for f in json.loads(run_design_md("lint", str(DESIGN)))["findings"] if f["severity"] != "info"]
    for finding in findings:
        print(f"DESIGN.md {finding['severity']} [{finding['rule']}]: {finding['message']}", file=sys.stderr)

    stale = False
    for flags, target in EXPORTS:
        expected = run_design_md("export", *flags, str(DESIGN))
        actual = target.read_text(encoding="utf-8")
        if actual != expected:
            stale = True
            rel = target.relative_to(ROOT)
            diff = difflib.unified_diff(
                actual.splitlines(keepends=True),
                expected.splitlines(keepends=True),
                fromfile=str(rel),
                tofile=f"generated:{rel}",
            )
            sys.stderr.writelines(diff)
            print(f"{rel} is out of date; run `mise run tokens`.", file=sys.stderr)

    return 1 if findings or stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
