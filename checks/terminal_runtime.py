#!/usr/bin/env python3
"""Check Ghostty's native configuration loader with an isolated home."""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    ghostty = shutil.which("ghostty")
    if not ghostty:
        raise RuntimeError("Install Ghostty to run its native configuration check")
    with tempfile.TemporaryDirectory(prefix="fmind-ghostty-") as directory:
        home = Path(directory)
        config = home / ".config/ghostty"
        config.mkdir(parents=True)
        shutil.copyfile(ROOT / "ghostty/fmind", config / "config")
        env = {"HOME": directory, "PATH": os.defpath, "LANG": "C.UTF-8"}
        for kind, path in (("CONFIG", ".config"), ("DATA", "data"), ("CACHE", "cache"), ("STATE", "state")):
            env[f"XDG_{kind}_HOME"] = str(home / path)
        result = subprocess.run(
            [ghostty, "+show-config"], env=env, capture_output=True, text=True, timeout=15, check=True
        )
        if result.stderr:
            raise RuntimeError("Ghostty emitted diagnostics: " + result.stderr)
        settings = dict(line.split(" = ", 1) for line in result.stdout.splitlines() if " = " in line)
        if float(settings.get("minimum-contrast", "1")) < 4.5:
            raise AssertionError("Ghostty did not enable the 4.5:1 contrast safeguard")
        print("Ghostty: native loader accepts the theme and enables minimum-contrast = 4.5")


if __name__ == "__main__":
    main()
