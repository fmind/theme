#!/usr/bin/env python3
"""Install a pinned parser/query runtime in the repository cache, never in Neovim's home."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVISION = "9a168f6357ed21c3a636e1727bc7d382abc451b8"
PLUGIN = ROOT / ".cache/syntax/nvim-treesitter"


def main() -> None:
    PLUGIN.mkdir(parents=True, exist_ok=True)
    if not (PLUGIN / ".git").exists():
        subprocess.run(["git", "init", "--quiet", str(PLUGIN)], check=True)
    current = subprocess.run(
        ["git", "-C", str(PLUGIN), "rev-parse", "HEAD"], capture_output=True, text=True, check=False
    )
    if current.stdout.strip() != REVISION:
        subprocess.run(
            [
                "git",
                "-C",
                str(PLUGIN),
                "fetch",
                "--depth=1",
                "https://github.com/nvim-treesitter/nvim-treesitter",
                REVISION,
            ],
            check=True,
            timeout=120,
        )
        subprocess.run(["git", "-C", str(PLUGIN), "checkout", "--detach", REVISION], check=True)
    dirty = subprocess.check_output(["git", "-C", str(PLUGIN), "status", "--porcelain"], text=True)
    if dirty:
        raise RuntimeError("Parser checkout has local changes; restore .cache/syntax/nvim-treesitter before setup")
    env = {**os.environ, "FMIND_THEME_ROOT": str(ROOT)}
    for kind in ("CONFIG", "DATA", "CACHE", "STATE"):
        env[f"XDG_{kind}_HOME"] = str(ROOT / ".cache/syntax" / kind.lower())
    subprocess.run(
        ["nvim", "--headless", "-u", "NONE", "-i", "NONE", "-l", str(ROOT / "checks/install.lua")],
        env=env,
        check=True,
        timeout=360,
    )


if __name__ == "__main__":
    main()
