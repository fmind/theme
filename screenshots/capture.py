#!/usr/bin/env python3
"""Capture real local terminals with VHS, a clean home and synthetic fixtures.

Run from any directory: python screenshots/capture.py
Requires installed vhs, ttyd, ffmpeg, bat, fish, nvim and zellij.
"""

from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
from contextlib import suppress
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], env: dict[str, str], cwd: Path, timeout: int = 90) -> None:
    with subprocess.Popen(command, env=env, cwd=cwd, start_new_session=True) as process:
        try:
            code = process.wait(timeout=timeout)
        finally:
            with suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGKILL)
        if code:
            raise RuntimeError(f"{command[0]} failed with exit {code}")


def main() -> None:
    tools = ["vhs", "ttyd", "ffmpeg", "bat", "fish", "nvim", "zellij"]
    binaries = {}
    for tool in tools:
        resolved = subprocess.run(["mise", "which", tool], capture_output=True, text=True, check=False)
        path = resolved.stdout.strip() if resolved.returncode == 0 else shutil.which(tool)
        if not path:
            raise RuntimeError(f"Install {tool} before recording")
        binaries[tool] = path
    font = Path(subprocess.check_output(["fc-match", "-f", "%{file}", "GoogleSansCode Nerd Font Mono"], text=True))
    if "GoogleSansCode" not in font.name:
        raise RuntimeError("Install GoogleSansCode Nerd Font Mono before recording")
    browser = os.environ.get("VHS_CHROME_PATH")
    if not browser:
        browsers = sorted((Path.home() / ".cache/ms-playwright").glob("chromium-*/chrome-linux*/chrome"))
        browser = str(browsers[-1]) if browsers else None
    if not browser or not Path(browser).is_file():
        raise RuntimeError("Set VHS_CHROME_PATH to Chromium or install Playwright Chromium before recording")
    with TemporaryDirectory(prefix="fmind-screenshots-") as directory:
        work = Path(directory)
        home = work / "home"
        config = home / ".config"
        for dest, source in {
            "nvim/colors/fmind.lua": "nvim/colors/fmind.lua",
            "fish/conf.d/theme.fish": "fish/fmind.fish",
            "bat/themes/fmind.tmTheme": "bat/fmind.tmTheme",
            "zellij/themes/fmind.kdl": "zellij/fmind.kdl",
        }.items():
            target = config / dest
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / source, target)
        fonts = home / ".local/share/fonts"
        fonts.mkdir(parents=True)
        for face in font.parent.glob("GoogleSansCodeNerdFontMono-*.ttf"):
            shutil.copyfile(face, fonts / face.name)
        for source in ("editor.lua", "demo.tape"):
            shutil.copyfile(ROOT / "screenshots" / source, work / source)
        for source in (ROOT / "checks/samples").glob("sample.*"):
            shutil.copyfile(source, work / source.name)
        (config / "bat/config").write_text('--theme="fmind"\n--paging=never\n')
        (work / "config.kdl").write_text('theme "fmind"\npane_frames true\ndefault_shell "fish"\n')
        (work / "shell.fish").write_text("""source ~/.config/fish/conf.d/theme.fish
function fish_prompt
    set_color green
    printf '> '
    set_color normal
end
clear
set_color blue --bold
printf 'Theme verification\\n\\n'
set_color green
printf '✓ Readable selections\\n✓ Visible pane frames\\n✓ Google-inspired colours\\n'
set_color normal
printf '\\nSynthetic local demonstration\\n'
""")
        (work / "layout.kdl").write_text("""layout {
    default_tab_template {
        pane size=1 borderless=true { plugin location="zellij:tab-bar"; }
        children
        pane size=2 borderless=true { plugin location="zellij:status-bar"; }
    }
    tab name="Code" focus=true {
        pane split_direction="vertical" {
            pane size="65%" name="Editor" command="nvim" { args "-u" "editor.lua" "-i" "NONE" "-n" "sample.py"; }
            pane name="Shell" command="fish" { args "--no-config" "-C" "source shell.fish"; }
        }
    }
    tab name="Review" { pane command="fish" { args "--no-config"; }; }
}
""")
        fields, slots = {}, {}
        for line in (ROOT / "ghostty/fmind").read_text().splitlines():
            key, separator, value = line.partition("=")
            if not separator or key.lstrip().startswith("#"):
                continue
            key, value = key.strip(), value.strip()
            if key == "palette":
                index, colour = value.split("=")
                slots[int(index)] = colour
            else:
                fields[key] = value
        names = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
        names += ["bright" + name.title() for name in names]
        theme = dict(zip(names, (slots[i] for i in range(16)), strict=True))
        theme.update(
            name="fmind",
            background=fields["background"],
            foreground=fields["foreground"],
            cursor=fields["cursor-color"],
            cursorAccent=fields["cursor-text"],
            selection=fields["selection-background"],
        )
        (work / "theme.tape").write_text("Set Theme " + json.dumps(theme) + "\n")
        env = {
            "FMIND_THEME_ROOT": str(ROOT),
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(config),
            "XDG_CACHE_HOME": str(home / ".cache"),
            "XDG_DATA_HOME": str(home / ".local/share"),
            "XDG_RUNTIME_DIR": str(work / "runtime"),
            "ZELLIJ_SOCKET_DIR": str(work / "sockets"),
            "PATH": ":".join(dict.fromkeys(str(Path(path).parent) for path in binaries.values())) + ":/usr/bin:/bin",
            "TERM": "xterm-256color",
            "COLORTERM": "truecolor",
            "LANG": "C.UTF-8",
            "TZ": "UTC",
            "PS1": "$ ",
            "HISTFILE": os.devnull,
            "VHS_CHROME_PATH": str(Path(browser).resolve()),
        }
        Path(env["XDG_RUNTIME_DIR"]).mkdir(mode=0o700)
        # Fail before recording if the checked parser runtime is absent or broken.
        run([binaries["nvim"], "--headless", "-u", "NONE", "-i", "NONE", "-l", "editor.lua"], env, work, 15)
        run([binaries["bat"], "cache", "--build"], env, work)
        run([binaries["vhs"], "validate", "demo.tape"], env, work, 15)
        try:
            run([binaries["vhs"], "demo.tape"], env, work)
        finally:
            # The capture has its own socket directory; never touch existing sessions.
            subprocess.run(
                [binaries["zellij"], "kill-session", "fmind-screenshot"],
                env=env,
                cwd=work,
                capture_output=True,
                timeout=10,
                check=False,
            )
        for name in ("zellij.png", "markdown.png"):
            source = work / name
            if not source.is_file():
                raise RuntimeError(f"VHS did not produce {name}")
        # Validate both outputs before replacing either retained screenshot.
        for name in ("zellij.png", "markdown.png"):
            shutil.copyfile(work / name, ROOT / "screenshots" / name)
        print("Captured code with search/selection, and Markdown")


if __name__ == "__main__":
    main()
