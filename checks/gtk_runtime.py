#!/usr/bin/env python3
"""Probe GTK 3 controls on a private Broadway display; no user theme is installed."""

from __future__ import annotations

import json
import os
import select
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def probe() -> None:
    import gi

    gi.require_version("Gtk", "3.0")
    gi.require_version("Gdk", "3.0")
    from gi.repository import Gdk, Gtk

    Gtk.init([])
    Gtk.Settings.get_default().set_property("gtk-enable-animations", False)
    provider = Gtk.CssProvider()
    provider.load_from_path(str(ROOT / "gtk/gtk-3.0/gtk.css"))
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
    window = Gtk.OffscreenWindow()
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    box.set_border_width(16)
    window.add(box)
    widgets = {
        "button": Gtk.Button(label="Continue"),
        "entry": Gtk.Entry(text="Synthetic selected text"),
        "spin": Gtk.SpinButton.new_with_range(0, 10, 1),
        "check": Gtk.CheckButton(label="Enabled option"),
        "radio": Gtk.RadioButton(label="Choice"),
        "switch": Gtk.Switch(),
        "disabled": Gtk.Button(label="Unavailable action"),
        "suggested": Gtk.Button(label="Confirm"),
        "destructive": Gtk.Button(label="Delete example"),
    }
    widgets["suggested"].get_style_context().add_class("suggested-action")
    widgets["destructive"].get_style_context().add_class("destructive-action")
    for widget in widgets.values():
        box.pack_start(widget, False, False, 0)
    widgets["disabled"].set_sensitive(False)
    window.show_all()
    while Gtk.events_pending():
        Gtk.main_iteration_do(False)
    pairs = []

    def color(value):
        assert value.alpha == 1, "Expected an opaque native control color"
        return "#" + "".join(f"{round(channel * 255):02x}" for channel in (value.red, value.green, value.blue))

    for name in ("button", "entry", "spin", "disabled", "suggested", "destructive"):
        widget = widgets[name]
        for state in (Gtk.StateFlags.NORMAL, Gtk.StateFlags.PRELIGHT, Gtk.StateFlags.FOCUSED):
            if name == "disabled":
                state = Gtk.StateFlags.INSENSITIVE
            context = widget.get_style_context()
            context.set_state(state)
            fg = color(context.get_property("color", state))
            bg = color(context.get_property("background-color", state))
            pairs.append((name, fg, bg, 4.5))
            if name in ("button", "entry", "spin"):
                pairs.append((name + " boundary", color(context.get_property("border-top-color", state)), bg, 3))
            if state == Gtk.StateFlags.FOCUSED:
                pairs.append((name + " focus", color(context.get_property("outline-color", state)), bg, 3))
    widgets["check"].set_active(True)
    widgets["radio"].set_active(True)
    widgets["switch"].set_active(True)
    assert all(widgets[name].get_active() for name in ("check", "radio", "switch"))
    widgets["entry"].select_region(0, 9)
    assert widgets["entry"].get_selection_bounds() == (0, 9)
    assert not widgets["disabled"].get_sensitive()
    window.destroy()
    print(json.dumps(pairs))


def main() -> None:
    from test_theme import contrast

    daemon = os.environ.get("BROADWAYD") or shutil.which("broadwayd")
    python = os.environ.get("GTK_PYTHON", "/usr/bin/python3")
    if not daemon:
        raise RuntimeError("Install GTK 3 broadwayd or set BROADWAYD to its binary; GTK_PYTHON must provide PyGObject")
    with tempfile.TemporaryDirectory(prefix="fmind-gtk-states-") as directory:
        work = Path(directory)
        env = {
            "HOME": directory,
            "PATH": os.defpath,
            "LANG": "C.UTF-8",
            "XDG_RUNTIME_DIR": directory,
            "XDG_CONFIG_HOME": str(work / "config"),
            "XDG_CACHE_HOME": str(work / "cache"),
            "XDG_DATA_HOME": str(work / "data"),
            "GDK_BACKEND": "broadway",
            "BROADWAY_DISPLAY": ":1",
            "NO_AT_BRIDGE": "1",
            "GSETTINGS_BACKEND": "memory",
            "G_DEBUG": "fatal-warnings",
        }
        with subprocess.Popen(
            [daemon, "--unixsocket", str(work / "http.socket"), ":1"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) as server:
            try:
                # Broadway uses an abstract socket on Linux, not a filesystem entry.
                if not select.select([server.stdout], [], [], 5)[0]:
                    raise RuntimeError("Private Broadway display failed to start")
                if not server.stdout.readline().startswith("Listening on "):
                    raise RuntimeError("Private Broadway display did not announce readiness")
                result = subprocess.run(
                    [python, str(Path(__file__).resolve()), "--probe"],
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=20,
                    check=False,
                )
                if result.returncode:
                    raise RuntimeError(f"GTK probe failed (exit {result.returncode}): {result.stderr}")
                if result.stderr:
                    raise RuntimeError("GTK probe emitted diagnostics: " + result.stderr)
                pairs = json.loads(result.stdout)
                failures = [
                    f"{name}: {fg} on {bg} falls below {threshold}:1"
                    for name, fg, bg, threshold in pairs
                    if contrast(fg, bg) < threshold
                ]
                if failures:
                    raise AssertionError("\n".join(failures))
            finally:
                server.terminate()
                _, errors = server.communicate(timeout=5)
                if errors:
                    raise RuntimeError("Broadway emitted diagnostics: " + errors)
        print(f"GTK 3: {len(pairs)} native color pairs and selection/toggle/disabled states passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--probe"]:
        probe()
    else:
        main()
