#!/usr/bin/env python3
"""Capture real local terminals with VHS, a clean home and synthetic fixtures.

Run from the repository root: mise run screenshots
Requires Linux, Fontconfig, Chromium, GoogleSansCode Nerd Font Mono, and the
tools pinned in screenshots/mise.toml.
"""

import os
import shutil
import signal
import subprocess
from collections.abc import Mapping, Sequence
from contextlib import suppress
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]


def run(command: Sequence[str], env: Mapping[str, str], cwd: Path, timeout: int = 90) -> None:
    with subprocess.Popen(
        command,
        env=env,
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    ) as process:
        try:
            code = process.wait(timeout=timeout)
        finally:
            with suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGKILL)
        if code:
            raise RuntimeError(f"{command[0]} failed with exit {code}")


def chromium_revision(path: Path) -> int:
    name = path.parent.parent.name.removeprefix("chromium-")
    return int(name) if name.isdigit() else -1


def atomic_copy(source: Path, target: Path) -> None:
    mode = target.stat().st_mode & 0o777 if target.exists() else 0o644
    with NamedTemporaryFile(dir=target.parent, prefix=f".{target.name}.", delete=False) as temp:
        temp_path = Path(temp.name)
        try:
            with source.open("rb") as src:
                shutil.copyfileobj(src, temp)
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


def main() -> None:
    tools = ["vhs", "ttyd", "ffmpeg", "bat", "fish", "nvim", "zellij"]
    binaries: dict[str, str] = {}
    for tool in tools:
        # `screenshots/mise.toml` tools are already first on PATH via `mise exec`.
        path = shutil.which(tool)
        if path and Path(path).parent.name == "shims":
            # Resolve shims before switching to the isolated HOME below.
            resolved = subprocess.run(
                ["mise", "which", tool],
                cwd=ROOT / "screenshots",
                capture_output=True,
                text=True,
                encoding="utf-8",
                stdin=subprocess.DEVNULL,
                timeout=15,
                check=False,
            )
            path = resolved.stdout.strip() if resolved.returncode == 0 else None
        if not path:
            raise RuntimeError(f"Install {tool} before recording (run `mise -C screenshots install`)")
        binaries[tool] = path
    font = Path(
        subprocess.check_output(
            ["fc-match", "-f", "%{file}", "GoogleSansCode Nerd Font Mono"],
            text=True,
            encoding="utf-8",
            stdin=subprocess.DEVNULL,
            timeout=15,
        )
    )
    if "GoogleSansCode" not in font.name:
        raise RuntimeError("Install GoogleSansCode Nerd Font Mono before recording")
    browser = os.environ.get("VHS_CHROME_PATH")
    if not browser:
        browsers = sorted(
            (Path.home() / ".cache/ms-playwright").glob("chromium-*/chrome-linux*/chrome"),
            key=chromium_revision,
        )
        browser = str(browsers[-1]) if browsers else None
    if not browser or not Path(browser).is_file():
        raise RuntimeError("Set VHS_CHROME_PATH to Chromium or install Playwright Chromium before recording")
    with TemporaryDirectory(prefix="fmind-screenshots-") as directory:
        work = Path(directory)
        home = work / "home"
        config = home / ".config"
        for dest, source in {
            "nvim/colors/fmind.lua": "nvim/colors/fmind.lua",
            "fish/themes/fmind.theme": "fish/themes/fmind.theme",
            "bat/themes/fmind.tmTheme": "bat/themes/fmind.tmTheme",
            "zellij/themes/fmind.kdl": "zellij/themes/fmind.kdl",
        }.items():
            target = config / dest
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / "themes" / source, target)
        fonts = home / ".local/share/fonts"
        fonts.mkdir(parents=True)
        for face in font.parent.glob("GoogleSansCodeNerdFontMono-*.ttf"):
            shutil.copyfile(face, fonts / face.name)
        for source in ("editor.lua", "demo.tape"):
            shutil.copyfile(ROOT / "screenshots" / source, work / source)
        for source in (ROOT / "screenshots/samples").glob("sample.*"):
            shutil.copyfile(source, work / source.name)
        (config / "bat/config").write_text('--theme="fmind"\n--paging=never\n', encoding="utf-8")
        (work / "preview.py").write_text(
            "# Numbered preview\ncount = 42\nmessage = 'Ready'\nprint(message)\n",
            encoding="utf-8",
        )
        (work / "config.kdl").write_text('theme "fmind"\npane_frames true\ndefault_shell "fish"\n', encoding="utf-8")
        (work / "shell.fish").write_text(
            """fish_config theme choose fmind
function fish_prompt
    set_color green
    printf '> '
    set_color normal
end
clear
set_color blue --bold
printf 'Theme verification\\n\\n'
set_color green
printf '✓ Readable selections\\n✓ Visible pane frames\\n✓ Google-inspired colors\\n'
set_color normal
printf '\\nSynthetic local demonstration\\n'
bat --style=numbers --color=always preview.py
""",
            encoding="utf-8",
        )
        (work / "layout.kdl").write_text(
            """layout {
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
""",
            encoding="utf-8",
        )
        shutil.copyfile(ROOT / "themes/vhs/fmind.tape", work / "theme.tape")
        env = {
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
        # Validate the isolated editor configuration before recording.
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
                stdin=subprocess.DEVNULL,
                timeout=10,
                check=False,
            )
        for name in ("zellij.png", "markdown.png"):
            source = work / name
            if not source.is_file():
                raise RuntimeError(f"VHS did not produce {name}")
        # Validate both outputs before atomically replacing either retained screenshot.
        for name in ("zellij.png", "markdown.png"):
            atomic_copy(work / name, ROOT / "screenshots" / name)
        print("Captured code with search/selection, and Markdown")


if __name__ == "__main__":
    main()
