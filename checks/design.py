"""Lint DESIGN.md and verify or regenerate CSS and Tailwind token files."""

import argparse
import difflib
import json
import os
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from tempfile import NamedTemporaryFile

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


def atomic_write(target: Path, content: str) -> None:
    """Write UTF-8 text atomically via a same-directory temporary file."""
    mode = target.stat().st_mode & 0o777 if target.exists() else 0o644
    with NamedTemporaryFile("w", dir=target.parent, prefix=f".{target.name}.", encoding="utf-8", delete=False) as temp:
        temp_path = Path(temp.name)
        try:
            temp.write(content)
            temp.flush()
            os.fsync(temp.fileno())
            temp_path.chmod(mode)
        except BaseException:
            temp_path.unlink(missing_ok=True)
            raise
    try:
        temp_path.replace(target)
    except BaseException:
        temp_path.unlink(missing_ok=True)
        raise


def main(argv: Sequence[str] | None = None) -> int:
    """Lint DESIGN.md (failing on warnings/errors) and verify or regenerate token files."""
    parser = argparse.ArgumentParser(
        description="Lint DESIGN.md and verify or regenerate CSS and Tailwind token files.",
        allow_abbrev=False,
        suggest_on_error=True,
    )
    parser.add_argument("--write", action="store_true", help="Regenerate CSS and Tailwind token files in place.")
    args = parser.parse_args(argv)

    if args.write:
        rendered = [(target, run_design_md("export", *flags, str(DESIGN))) for flags, target in EXPORTS]
        for target, content in rendered:
            atomic_write(target, content)
        return 0

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
