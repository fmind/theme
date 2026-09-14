"""Check launcher, lock-screen and desktop state colors without a live session."""

import configparser
import json
import os
import re
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path

import tinycss2
from test_theme import PALETTE, ROOT, contrast


def ini(path, root=False):
    parser = configparser.ConfigParser(interpolation=None)
    content = (ROOT / path).read_text()
    parser.read_string(("[main]\n" if root else "") + content)
    return parser


class WaylandPortTests(unittest.TestCase):
    def readable(self, fg, bg, label=""):
        for color in (fg, bg):
            self.assertIn(color, PALETTE["official"] + PALETTE["custom"], label)
        self.assertGreaterEqual(contrast(fg, bg), 4.5, label)

    def test_fuzzel_rgba_roles_and_selected_matches(self):
        colors = dict(ini("fuzzel/fmind.ini")["colors"])
        self.assertEqual(
            set(colors),
            {
                "background",
                "text",
                "message",
                "prompt",
                "placeholder",
                "input",
                "match",
                "selection",
                "selection-text",
                "selection-match",
                "counter",
                "border",
            },
        )
        for name, value in colors.items():
            self.assertRegex(value, r"^[0-9a-f]{6}ff$", name)
        for name in ("text", "message", "prompt", "placeholder", "input", "match", "counter"):
            self.readable("#" + colors[name][:6], "#" + colors["background"][:6], name)
        for name in ("selection-text", "selection-match"):
            self.readable("#" + colors[name][:6], "#" + colors["selection"][:6], name)

    def test_swaylock_all_indicator_states_and_no_policy(self):
        colors = dict(ini("swaylock/fmind.conf", root=True)["main"])
        self.assertEqual(colors.pop("font"), "Google Sans")
        expected = {
            "color",
            "key-hl-color",
            "bs-hl-color",
            "caps-lock-key-hl-color",
            "caps-lock-bs-hl-color",
            "separator-color",
            "layout-bg-color",
            "layout-border-color",
            "layout-text-color",
        }
        for state in ("", "clear-", "caps-lock-", "ver-", "wrong-"):
            for part in ("inside", "line", "ring", "text"):
                expected.add(f"{part}-{state}color")
            self.readable("#" + colors[f"text-{state}color"], "#" + colors[f"inside-{state}color"], state)
        # The allowlist prevents accidentally adding grace periods or effects-fork options.
        self.assertEqual(set(colors), expected)
        for value in colors.values():
            self.assertRegex(value, r"^[0-9a-f]{6}$")
        self.readable("#" + colors["layout-text-color"], "#" + colors["layout-bg-color"])

    def test_hyprland_lua_runs_with_only_configuration_api(self):
        program = """
local config
local chunk = assert(loadfile(arg[1]))
setfenv(chunk, {hl = {config = function(value)
  assert(config == nil, "multiple config calls")
  config = value
end}})
chunk()
io.write(vim.json.encode(config))
"""
        with tempfile.TemporaryDirectory(prefix="fmind-hyprland-") as home:
            script = Path(home) / "check.lua"
            script.write_text(program)
            result = subprocess.run(
                ["nvim", "--headless", "-u", "NONE", "-i", "NONE", "-l", str(script), str(ROOT / "hyprland/fmind.lua")],
                env={
                    **os.environ,
                    "HOME": home,
                    "XDG_CONFIG_HOME": home,
                    "XDG_CACHE_HOME": home,
                    "XDG_DATA_HOME": home,
                    "XDG_STATE_HOME": home,
                },
                capture_output=True,
                text=True,
                check=True,
                timeout=15,
            )
        self.assertEqual(result.stderr, "")
        config = json.loads(result.stdout)
        self.assertEqual(set(config), {"general", "decoration", "group", "misc"})
        bar = config["group"]["groupbar"]
        self.assertTrue(bar["gradients"])
        for state, text in (
            ("active", "text_color"),
            ("inactive", "text_color_inactive"),
            ("locked_active", "text_color_locked_active"),
            ("locked_inactive", "text_color_locked_inactive"),
        ):
            fg, bg = bar[text], bar["col"][state]
            for color in (fg, bg):
                self.assertRegex(color, r"^rgba\([0-9a-f]{6}ff\)$")
            self.readable("#" + fg[5:11], "#" + bg[5:11], state)
        self.assertEqual(config["misc"]["background_color"], "rgba(ffffffff)")

    def test_hyprlock_visual_widgets_and_readable_password(self):
        content = (ROOT / "hyprland/hyprlock.conf").read_text()
        blocks = re.findall(r"(?m)^([\w-]+) \{\n([^}]+)\}", content)
        self.assertEqual([name for name, _ in blocks], ["background", "input-field", "label"])
        self.assertNotRegex(content, r"(?m)^\s*(auth|general|source|grace|exec)\b")
        self.assertNotIn("cmd[", content)
        values = dict(line.strip().split(" = ", 1) for line in blocks[1][1].splitlines() if " = " in line)
        self.assertGreater(int(values["outline_thickness"]), 0)
        self.readable("#" + values["font_color"][5:11], "#" + values["inner_color"][5:11])
        for color in re.findall(r"rgba\(([^)]+)\)", content):
            self.assertRegex(color, r"^[0-9a-f]{6}ff$")
            self.assertIn("#" + color[:6], PALETTE["official"] + PALETTE["custom"])

    def test_polybar_and_wob_color_references(self):
        colors = ini("polybar/fmind.ini")["colors"]
        for fg in ("foreground", "primary", "secondary", "alert", "disabled"):
            for bg in ("background", "background-alt"):
                self.readable(colors[fg], colors[bg], fg)
        wob = ini("wob/fmind.ini", root=True)["main"]
        self.assertEqual(
            set(wob),
            {
                "border_color",
                "background_color",
                "bar_color",
                "overflow_border_color",
                "overflow_background_color",
                "overflow_bar_color",
            },
        )
        # These are graphics; 4.5:1 exceeds the non-text minimum and keeps low levels visible.
        for prefix in ("", "overflow_"):
            self.readable(wob[prefix + "bar_color"], wob[prefix + "background_color"])

    def test_dmenu_native_scheme_pairs(self):
        source = (ROOT / "dmenu/fmind.h").read_text()
        schemes = re.findall(r'\[(Scheme\w+)\]\s*=\s*\{\s*"(#[\da-f]{6})",\s*"(#[\da-f]{6})"\s*\}', source)
        self.assertEqual({name for name, _, _ in schemes}, {"SchemeNorm", "SchemeSel", "SchemeOut"})
        for name, fg, bg in schemes:
            self.readable(fg, bg, name)

    def test_bspwm_sources_only_four_border_settings(self):
        with tempfile.TemporaryDirectory(prefix="fmind-bspwm-") as home:
            script = Path(home) / "check.sh"
            script.write_text('bspc() { printf "%s\\n" "$@"; }\n. ' + shlex.quote(str(ROOT / "bspwm/fmind.sh")) + "\n")
            result = subprocess.run(
                ["sh", str(script)],
                capture_output=True,
                text=True,
                check=True,
                env={**os.environ, "HOME": home},
                timeout=10,
            )
        self.assertEqual(result.stderr, "")
        args = result.stdout.splitlines()
        self.assertEqual(args[::3], ["config"] * 4)
        self.assertEqual(
            set(args[1::3]),
            {"normal_border_color", "active_border_color", "focused_border_color", "presel_feedback_color"},
        )
        self.assertEqual(len(args), 12)
        for color in args[2::3]:
            self.assertIn(color, PALETTE["official"] + PALETTE["custom"])

    def test_gtk_stylesheets_parse_and_text_colors_survive_highlights(self):
        for app in ("wofi", "swayosd", "swaync"):
            rules = tinycss2.parse_stylesheet(
                (ROOT / app / "fmind.css").read_text(), skip_comments=True, skip_whitespace=True
            )
            styles = {}
            for rule in rules:
                self.assertEqual(rule.type, "qualified-rule", app)
                declarations = tinycss2.parse_declaration_list(rule.content, skip_comments=True, skip_whitespace=True)
                selector = tinycss2.serialize(rule.prelude).strip()
                styles[selector] = {}
                for declaration in declarations:
                    self.assertEqual(declaration.type, "declaration", selector)
                    value = tinycss2.serialize(declaration.value).strip()
                    styles[selector][declaration.name] = value
                    if declaration.name == "color" and value.startswith("#"):
                        for bg in ("#ffffff", "#f1f3f4", "#d2e3fc"):
                            self.readable(value, bg, app + ": " + selector)
            if app == "swayosd":
                self.assertTrue(any("segment.active" in selector for selector in styles))
            if app == "swaync":
                variables = styles[":root"]
                self.assertEqual(variables["--noti-bg"], "255, 255, 255")
                self.assertEqual(variables["--noti-bg-alpha"], "1")
                for text in ("--text-color", "--text-color-disabled"):
                    for bg in (
                        "--cc-bg",
                        "--noti-bg-darker",
                        "--noti-bg-hover",
                        "--noti-bg-focus",
                        "--noti-close-bg",
                        "--noti-close-bg-hover",
                        "--bg-selected",
                        "--mpris-album-art-overlay",
                    ):
                        self.readable(variables[text], variables[bg], text + ": " + bg)
