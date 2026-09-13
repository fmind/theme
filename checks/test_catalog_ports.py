"""Parse the additional free-catalog ports and check their actual color pairs."""

import ast
import configparser
import json
import re
import tomllib
import unittest
import xml.etree.ElementTree as ET

import tinycss2
from configobj import ConfigObj
from test_theme import PALETTE, ROOT, contrast

ANSI = list(PALETTE["ansi"].values())
COLORS = set(PALETTE["official"] + PALETTE["custom"])


def read(path):
    return (ROOT / path).read_text()


def ini(path, section=None):
    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str
    parser.read_string((f"[{section}]\n" if section else "") + read(path))
    return parser


def rgb(value):
    channels = [int(c) for c in value.split(",")] if isinstance(value, str) else value
    if len(channels) != 3 or any(not 0 <= c <= 255 for c in channels):
        raise ValueError("Invalid RGB color")
    return "#" + "".join(f"{c:02x}" for c in channels)


class CatalogPortTests(unittest.TestCase):
    def readable(self, fg, bg, label=""):
        self.assertIn(fg, COLORS)
        self.assertIn(bg, COLORS)
        self.assertGreaterEqual(contrast(fg, bg), 4.5, label)

    def test_gnome_terminal_profile(self):
        profile = ini("gnome-terminal/fmind.dconf")["/"]
        self.assertEqual(ast.literal_eval(profile["palette"]), ANSI)
        self.assertEqual(profile["use-theme-colors"], "false")
        for prefix in ("", "highlight-", "cursor-"):
            self.readable(
                ast.literal_eval(profile[prefix + "foreground-color"]),
                ast.literal_eval(profile[prefix + "background-color"]),
                prefix,
            )

    def test_other_terminal_palettes(self):
        terminator = ConfigObj(read("terminator/fmind.conf").splitlines())["profiles"]["fmind"]
        self.assertEqual(terminator["palette"].split(":"), ANSI)
        self.readable(terminator["foreground_color"], terminator["background_color"])
        xfce = ini("xfce4-terminal/fmind.theme")["Scheme"]
        self.assertEqual(xfce["ColorPalette"].split(";"), ANSI)
        self.readable(xfce["ColorForeground"], xfce["ColorBackground"])
        self.readable(xfce["ColorForeground"], xfce["ColorSelection"])
        mintty = ini("mintty/fmind.minttyrc", "colors")["colors"]
        names = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]
        self.assertEqual([rgb(mintty[p + n]) for p in ("", "Bold") for n in names], ANSI)
        self.assertLessEqual({rgb(value) for value in mintty.values()}, COLORS)
        self.readable(rgb(mintty["HighlightForegroundColour"]), rgb(mintty["HighlightBackgroundColour"]))
        termux = ini("termux/colors.properties", "colors")["colors"]
        self.assertEqual([termux[f"color{i}"] for i in range(16)], ANSI)
        self.readable(termux["foreground"], termux["background"])
        xresources = dict(re.findall(r"(?m)^\*\.([\w]+): (#[\da-f]{6})$", read("xresources/fmind.Xresources")))
        self.assertEqual([xresources[f"color{i}"] for i in range(16)], ANSI)
        self.readable(xresources["foreground"], xresources["background"])
        hyper = json.loads(read("hyper/fmind.json"))
        self.assertEqual(list(hyper["colors"].values()), ANSI)
        self.readable(hyper["foregroundColor"], hyper["backgroundColor"])
        self.readable(hyper["cursorAccentColor"], hyper["cursorColor"])
        for color in hyper["colors"].values():
            self.readable(color, hyper["selectionColor"])

    def test_browser_manifests(self):
        for app in ("chrome", "firefox"):
            manifest = json.loads(read(app + "/manifest.json"))
            self.assertNotIn("permissions", manifest)
            self.assertNotIn("content_scripts", manifest)
            self.assertNotIn("background", manifest)
            self.assertEqual(manifest["manifest_version"], 3 if app == "chrome" else 2)
            colors = manifest["theme"]["colors"]
            colors = {key: rgb(value) if isinstance(value, list) else value for key, value in colors.items()}
            self.assertLessEqual(set(colors.values()), COLORS)
            for fg, bg in (("tab_text", "toolbar"), ("tab_background_text", "frame"), ("ntp_text", "ntp_background")):
                self.readable(colors[fg], colors[bg], app + ": " + fg)
            if app == "firefox":
                for bg in (
                    "popup",
                    "popup_highlight",
                    "sidebar",
                    "sidebar_highlight",
                    "toolbar_field",
                    "toolbar_field_highlight",
                ):
                    self.readable(colors[bg + "_text"], colors[bg], bg)

    def test_kate_style_roles(self):
        theme = json.loads(read("kate/fmind.theme"))
        colors = theme["editor-colors"]
        self.assertEqual(theme["metadata"]["name"], "Fmind")
        self.assertGreaterEqual(len(theme["text-styles"]), 31)
        for name, style in theme["text-styles"].items():
            for bg in ("BackgroundColor", "CurrentLine", "SearchHighlight", "ReplaceHighlight"):
                self.readable(style["text-color"], colors[bg], name)
            self.readable(style["selected-text-color"], colors["TextSelection"], name)

    def test_gtksourceview_styles(self):
        root = ET.fromstring(read("gedit/fmind.xml"))
        self.assertEqual(root.tag, "style-scheme")
        self.assertEqual(root.attrib["id"], "fmind")
        styles = {s.attrib["name"]: s.attrib for s in root.findall("style")}
        self.assertEqual(len(styles), len(root.findall("style")))
        for name, style in styles.items():
            if "foreground" in style and name != "cursor" and name != "draw-spaces" and name != "right-margin":
                self.readable(style["foreground"], style.get("background", styles["text"]["background"]), name)
            if name.startswith("def:"):
                for surface in ("selection", "current-line", "search-match"):
                    self.readable(style["foreground"], styles[surface]["background"], name)

    def test_jetbrains_defaults_and_highlights(self):
        root = ET.fromstring(read("jetbrains/fmind.icls"))
        self.assertEqual(root.tag, "scheme")
        self.assertEqual(root.attrib["parent_scheme"], "Default")
        colors = {v.attrib["name"]: "#" + v.attrib["value"] for v in root.findall("./colors/option")}
        attributes = {
            a.attrib["name"]: {v.attrib["name"]: v.attrib["value"] for v in a.findall("./value/option")}
            for a in root.findall("./attributes/option")
        }
        self.assertEqual(len(attributes), len(root.findall("./attributes/option")))
        self.readable(colors["SELECTION_FOREGROUND"], colors["SELECTION_BACKGROUND"])
        backgrounds = [
            "#" + attributes["TEXT"]["BACKGROUND"],
            colors["CARET_ROW_COLOR"],
            colors["SELECTION_BACKGROUND"],
        ]
        backgrounds += [
            "#" + attributes[name]["BACKGROUND"] for name in ("DIFF_INSERTED", "DIFF_DELETED", "DIFF_MODIFIED")
        ]
        for name, value in attributes.items():
            if "FOREGROUND" in value:
                for bg in ["#" + value["BACKGROUND"]] if "BACKGROUND" in value else backgrounds:
                    self.readable("#" + value["FOREGROUND"], bg, name)

    def test_emacs_face_forms_and_colors(self):
        source = read("emacs/fmind-theme.el")
        self.assertIn("(provide-theme 'fmind)", source)
        faces = {}
        for line in source.splitlines():
            if not line.startswith(" '("):
                continue
            match = re.fullmatch(r" '\(([\w-]+) \(\(t \(([^()]+)\)\)\)\)", line)
            self.assertIsNotNone(match, line)
            self.assertNotIn(match[1], faces)
            faces[match[1]] = dict(re.findall(r':(foreground|background) "(#[\da-f]{6})"', match[2]))
        self.assertGreaterEqual(len(faces), 60)
        for name, face in faces.items():
            if "foreground" in face:
                self.readable(face["foreground"], face.get("background", faces["default"]["background"]), name)
                if name.startswith("font-lock-"):
                    for surface in ("region", "hl-line", "diff-added", "diff-removed"):
                        self.readable(face["foreground"], faces[surface]["background"], name)

    def test_notification_window_and_pdf_styles(self):
        dunst = ini("dunst/fmind.conf")
        for section in ("urgency_low", "urgency_normal", "urgency_critical"):
            self.readable(dunst[section]["foreground"].strip('"'), dunst[section]["background"].strip('"'), section)
        for line in read("i3/fmind.conf").splitlines():
            if line.startswith("client.") and not line.startswith("client.background"):
                name, border, bg, fg, indicator, child = line.split()
                self.readable(fg, bg, name)
                self.assertTrue({border, indicator, child} <= COLORS)
        fields = dict(re.findall(r'(?m)^set ([\w-]+) "(#[\da-f]{6})"$', read("zathura/fmind.conf")))
        for name, bg in fields.items():
            if name.endswith("-bg"):
                self.readable(fields[name[:-3] + "-fg"], bg, name)

    def test_shell_input_colors(self):
        for fg in re.findall(r"fg=(#[\da-f]{6})", read("zsh-syntax-highlighting/fmind.zsh")):
            self.readable(fg, PALETTE["ground"])
        ps = read("powershell/fmind.ps1")
        styles = re.findall(r'(?m)^    (\w+) = "`e\[38;2;(\d+);(\d+);(\d+)(?:;48;2;(\d+);(\d+);(\d+))?m"$', ps)
        self.assertEqual(len(styles), 18)
        for name, red, green, blue, br, bg, bb in styles:
            fg = rgb([int(red), int(green), int(blue)])
            background = rgb([int(br), int(bg), int(bb)]) if br else PALETTE["ground"]
            self.readable(fg, background, name)

    def test_css_documents_and_color_pairs(self):
        for path in ("obsidian/theme.css", "typora/fmind.css", "waybar/fmind.css", "rofi/fmind.rasi"):
            variables = {}
            for rule in tinycss2.parse_stylesheet(read(path), skip_comments=True, skip_whitespace=True):
                self.assertEqual(rule.type, "qualified-rule", path)
                declarations = tinycss2.parse_declaration_list(rule.content, skip_comments=True, skip_whitespace=True)
                fields = {}
                for decl in declarations:
                    self.assertEqual(decl.type, "declaration", path)
                    fields[decl.name] = tinycss2.serialize(decl.value).strip()
                variables.update({k: v for k, v in fields.items() if k.startswith("--")})
                fg = fields.get("color", fields.get("text-color"))
                bg = fields.get("background", fields.get("background-color"))
                if fg and bg and fg.startswith("#") and bg.startswith("#"):
                    self.readable(fg, bg, path)
            if path.startswith("obsidian"):
                for key in (
                    "--text-normal",
                    "--text-muted",
                    "--text-faint",
                    "--code-comment",
                    "--code-function",
                    "--code-string",
                    "--code-value",
                ):
                    for bg in (
                        "--background-primary",
                        "--background-secondary",
                        "--text-selection",
                        "--text-highlight-bg",
                    ):
                        self.readable(variables[key], variables[bg], key)
                self.readable(variables["--text-on-accent"], variables["--interactive-accent"])
                self.readable(variables["--tag-color"], variables["--tag-background"])
            if path.startswith("typora"):
                for fg, bg in (
                    ("--text-color", "--bg-color"),
                    ("--active-file-text-color", "--active-file-bg-color"),
                    ("--select-text-font-color", "--select-text-bg-color"),
                    ("--search-select-text-color", "--search-select-bg-color"),
                ):
                    self.readable(variables[fg], variables[bg], fg)

    def test_python_tool_styles(self):
        theme = tomllib.loads(read("streamlit/fmind.toml"))["theme"]
        self.assertEqual(theme["base"], "light")
        self.readable(theme["textColor"], theme["backgroundColor"])
        self.readable(theme["textColor"], theme["secondaryBackgroundColor"])
        self.readable(theme["codeTextColor"], theme["codeBackgroundColor"])
        self.readable("#ffffff", theme["primaryColor"])
        for color in theme["chartCategoricalColors"]:
            self.readable(color, theme["backgroundColor"])
        rc = dict(
            line.split(":", 1)
            for line in read("matplotlib/fmind.mplstyle").splitlines()
            if line and not line.startswith("#")
        )
        for key in ("text.color", "axes.labelcolor", "axes.titlecolor", "xtick.color", "ytick.color"):
            self.readable("#" + rc[key].strip(), "#" + rc["axes.facecolor"].strip(), key)
