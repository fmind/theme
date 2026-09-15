"""Parse the additional free-catalog ports and check their actual color pairs."""

import ast
import configparser
import json
import plistlib
import re
import struct
import tomllib
import unittest
import xml.etree.ElementTree as ET

import tinycss2
import yaml
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
        terminator_lines = read("terminator/fmind.conf").splitlines()
        terminator = dict(line.strip().split(" = ", 1) for line in terminator_lines if " = " in line)
        terminator["palette"] = terminator["palette"].strip('"')
        terminator["foreground_color"] = terminator["foreground_color"].strip('"')
        terminator["background_color"] = terminator["background_color"].strip('"')
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

    def test_cursor_and_vscode_derivatives(self):
        pkg = json.loads(read("cursor/package.json"))
        self.assertEqual(pkg["name"], "fmind-cursor")
        theme_path = pkg["contributes"]["themes"][0]["path"]
        theme = json.loads(read("cursor/" + theme_path.lstrip("./")))
        self.assertEqual(theme["type"], "light")
        self.readable(theme["colors"]["foreground"], theme["colors"]["editor.background"])

    def test_monkeytype_theme(self):
        config = json.loads(read("monkeytype/fmind.json"))
        self.assertEqual(config["name"], "Fmind")
        self.assertLessEqual(set(config.values()) - {"Fmind"}, COLORS)
        self.readable(config["textColor"], config["bgColor"])
        self.readable(config["mainColor"], config["bgColor"])

    def test_slack_palette(self):
        values = [c.strip() for c in read("slack/fmind.txt").strip().split(",")]
        self.assertEqual(len(values), 8)
        self.assertLessEqual(set(values), COLORS)
        self.readable(values[5], values[0])
        self.readable(values[3], values[2])

    def test_raycast_theme(self):
        data = json.loads(read("raycast/fmind.json"))
        self.assertEqual(data["appearance"], "light")
        colors = data["colors"]
        self.assertLessEqual(set(colors.values()), COLORS)
        self.readable(colors["text"], colors["background"])
        self.readable(colors["text"], colors["backgroundSecondary"])
        self.readable(colors["text"], colors["selection"])

    def test_claude_code_config(self):
        cfg = json.loads(read("claude-code/config.json"))
        self.assertEqual(cfg["theme"], "light-ansi")

    def test_zsh_theme(self):
        source = read("zsh/fmind.zsh-theme")
        hex_codes = set(re.findall(r"%F{(#[0-9a-fA-F]{6})}", source))
        self.assertLessEqual(hex_codes, COLORS)
        for code in hex_codes:
            self.readable(code, "#ffffff")

    def test_alfred_theme(self):
        colors = json.loads(read("alfred/fmind.alfredappearance"))["alfredtheme"]["theme"]["color"]
        for key, val in colors.items():
            self.assertIn(val, COLORS, f"Alfred {key}")
        self.readable(colors["resultText"], colors["background"])
        self.readable(colors["resultSelectedText"], colors["resultSelectedBackground"])
        self.readable(colors["shortcutSelectedText"], colors["resultSelectedBackground"])

    def test_betterdiscord_theme(self):
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", read("betterdiscord/fmind.theme.css")))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_cmder_scheme(self):
        root = ET.fromstring(read("cmder/fmind.xml"))
        for val in root.findall(".//value"):
            if val.attrib.get("type") == "dword":
                data = val.attrib["data"]
                bgr = data[2:]
                rgb = "#" + bgr[4:6] + bgr[2:4] + bgr[0:2]
                self.assertIn(rgb.lower(), COLORS, f"Cmder {data}")

    def test_gmk_scheme(self):
        groups = json.loads(read("gmk/fmind.json"))["colors"]
        for name, vals in groups.items():
            self.readable(vals["legend"], vals["background"], f"gmk {name}")

    def test_highlightjs_theme(self):
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", read("highlightjs/fmind.css")))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_insomnia_plugin(self):
        pkg = json.loads(read("insomnia/package.json"))
        self.assertEqual(pkg["name"], "insomnia-plugin-theme-fmind")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", read("insomnia/index.js")))
        self.assertLessEqual(hex_codes, COLORS)

    def test_mysql_workbench_scheme(self):
        root = ET.fromstring(read("mysql-workbench/code_editor.xml"))
        styles = root.findall("style")
        self.assertGreater(len(styles), 0)
        for st in styles:
            fg = st.attrib["fore-color-light"]
            bg = st.attrib["back-color-light"]
            self.assertIn(fg, COLORS)
            self.assertIn(bg, COLORS)

    def test_oracle_sql_developer_scheme(self):
        root = ET.fromstring(read("oracle-sql-developer/Fmind.xml"))
        items = [i for i in root.findall(".//Item") if "frgb" in i.attrib]
        self.assertGreater(len(items), 0)
        for item in items:
            fg = f"#{(int(item.attrib['frgb']) & 0xFFFFFF):06x}"
            bg = f"#{(int(item.attrib['brgb']) & 0xFFFFFF):06x}"
            self.readable(fg, bg, item.attrib.get("name", ""))

    def test_powerlevel10k_theme(self):
        source = read("powerlevel10k/p10k-fmind.zsh")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", source))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#d2e3fc")
        self.readable("#0d652d", "#ceead6")
        self.readable("#934900", "#feefc3")
        self.readable("#a50e0e", "#fad2cf")

    def test_qbittorrent_theme(self):
        colors = json.loads(read("qbittorrent/config.json"))["colors"]
        for key, val in colors.items():
            self.readable(val, "#ffffff", f"qbittorrent {key}")
        qss_hex = set(re.findall(r"#[0-9a-fA-F]{6}", read("qbittorrent/stylesheet.qss")))
        self.assertLessEqual(qss_hex, COLORS)

    def test_steam_skin(self):
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", read("steam/webkit.css")))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_telegram_palette(self):
        source = read("telegram/colors.tdesktop-palette")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", source))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")
        self.readable("#ffffff", "#174ea6")

    def test_visual_studio_settings(self):
        root = ET.fromstring(read("visual-studio/fmind.vssettings"))
        items = root.findall(".//Item")
        self.assertGreater(len(items), 0)
        for item in items:
            fg_raw = item.attrib["Foreground"]
            bg_raw = item.attrib["Background"]
            if fg_raw.startswith("0x00"):
                fg = "#" + fg_raw[8:10] + fg_raw[6:8] + fg_raw[4:6]
                self.assertIn(fg.lower(), COLORS)
            if bg_raw.startswith("0x00"):
                bg = "#" + bg_raw[8:10] + bg_raw[6:8] + bg_raw[4:6]
                self.assertIn(bg.lower(), COLORS)

    def test_vivaldi_theme(self):
        theme = json.loads(read("vivaldi/fmind.json"))["theme"]
        self.assertEqual(theme["name"], "Fmind")
        self.readable(theme["foreground"], theme["background"])
        self.readable(theme["accent"], theme["background"])

    def test_wallpaper_svg(self):
        svg = ET.fromstring(read("wallpaper/fmind.svg"))
        self.assertEqual(svg.attrib["width"], "3840")
        self.assertEqual(svg.attrib["height"], "2160")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", read("wallpaper/fmind.svg")))
        self.assertLessEqual(hex_codes, COLORS)

    def test_telegram_android_theme(self):
        source = read("telegram-android/fmind.attheme")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", source))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")
        self.readable("#174ea6", "#d2e3fc")

    def test_gh_pages_theme(self):
        css = read("gh-pages/assets/css/style.css")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", css))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_libreoffice_palette(self):
        root = ET.fromstring(read("libreoffice/fmind.soc"))
        colors = {
            elem.attrib.get("{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}color")
            for elem in root.findall(".//{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}color")
        }
        self.assertLessEqual(colors, COLORS)
        self.assertEqual(len(colors), 20)

    def test_arduino_ide_theme(self):
        source = read("arduino-ide/theme.txt")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", source))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")
        self.readable("#ffffff", "#a50e0e")

    def test_midnight_commander_skin(self):
        source = read("midnight-commander/fmind.ini")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", source))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")
        self.readable("#ffffff", "#174ea6")

    def test_godot_syntax_theme(self):
        source = read("godot/fmind.tet")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", source))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_sequel_pro_colors(self):
        theme = plistlib.loads((ROOT / "sequel-pro/Fmind.spColor").read_bytes())
        self.assertLessEqual(set(theme.values()), COLORS)
        self.readable(theme["text-color"], theme["background-color"])
        self.readable(theme["keyword-color"], theme["background-color"])

    def test_duckduckgo_style(self):
        css = read("duckduckgo/fmind.user.css")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", css))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")
        self.readable("#174ea6", "#ffffff")

    def test_github_style(self):
        css = read("github/fmind.user.css")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", css))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")
        self.readable("#ffffff", "#174ea6")

    def test_gamepad_viewer_style(self):
        css = read("gamepad-viewer/fmind.css")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", css))
        self.assertLessEqual(hex_codes, COLORS)

    def test_spotify_tui_theme(self):
        data = yaml.safe_load(read("spotify-tui/fmind.yml"))["theme"]
        self.assertLessEqual(set(data.values()), COLORS)
        self.readable(data["text"], data["selected"])

    def test_telegram_ios_theme(self):
        data = json.loads(read("telegram-ios/fmind.tgcolors"))["colors"]
        self.assertLessEqual(set(data.values()), COLORS)
        self.readable(data["incomingText"], data["incomingBubble"])
        self.readable(data["outgoingText"], data["outgoingBubble"])

    def test_gamemaker_studio_theme(self):
        data = json.loads(read("gamemaker-studio/fmind.json"))["editor_colours"]
        self.assertLessEqual(set(data.values()), COLORS)
        self.readable(data["text"], data["background"])
        self.readable(data["keywords"], data["background"])

    def test_monodevelop_scheme(self):
        data = json.loads(read("monodevelop/Fmind.json"))["colors"]
        self.assertLessEqual(set(data.values()), COLORS)
        self.readable(data["Plain Text"], data["Background"])
        self.readable(data["Selected Text"], data["Selected Background"])

    def test_youtube_style(self):
        css = read("youtube/fmind.user.css")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", css))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")
        self.readable("#ffffff", "#174ea6")

    def test_hacker_news_style(self):
        css = read("hacker-news/fmind.user.css")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", css))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_blender_theme(self):
        content = read("blender/fmind.xml")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", content))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_adobe_swatches(self):
        data = json.loads(read("adobe/swatches.json"))
        colors = {s["hex"] for s in data["swatches"]}
        self.assertEqual(colors, COLORS)
        binary = (ROOT / "adobe/Fmind.ase").read_bytes()
        signature, major, minor, count = struct.unpack_from(">4sHHI", binary)
        self.assertEqual((signature, major, minor, count), (b"ASEF", 1, 0, len(data["swatches"])))
        offset = 12
        decoded = []
        for _ in range(count):
            kind, size = struct.unpack_from(">HI", binary, offset)
            self.assertEqual(kind, 1, "Expected an ASE color block")
            offset += 6
            end = offset + size
            length = struct.unpack_from(">H", binary, offset)[0]
            offset += 2
            name = binary[offset : offset + length * 2].decode("utf-16-be")
            self.assertTrue(name.endswith("\0"))
            offset += length * 2
            self.assertEqual(binary[offset : offset + 4], b"RGB ")
            red, green, blue, color_type = struct.unpack_from(">fffH", binary, offset + 4)
            self.assertEqual(color_type, 2, "Expected normal document swatches")
            for channel in (red, green, blue):
                self.assertTrue(0 <= channel <= 1)
            decoded.append({"name": name[:-1], "hex": rgb([round(c * 255) for c in (red, green, blue)])})
            offset += 18
            self.assertEqual(offset, end, "Incorrect ASE block length")
        self.assertEqual(offset, len(binary), "Unexpected trailing ASE data")
        self.assertEqual(decoded, data["swatches"])

    def test_oh_my_posh_theme(self):
        content = read("oh-my-posh/fmind.omp.json")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", content))
        self.assertLessEqual(hex_codes, COLORS)

    def test_grub_theme(self):
        content = read("grub/theme.txt")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", content))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_pythonista_theme(self):
        data = json.loads(read("pythonista/Fmind.json"))
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", read("pythonista/Fmind.json"))}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["text"], data["background"])

    def test_gitk_colors(self):
        content = read("gitk/fmind.gitk")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_qutebrowser_theme(self):
        content = read("qutebrowser/fmind.py")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_figma_tokens(self):
        data = json.loads(read("figma/tokens.json"))["Fmind"]
        hex_codes = {v["value"].lower() for v in data.values()}
        self.assertLessEqual(hex_codes, COLORS)

    def test_wox_theme(self):
        content = read("wox/Fmind.xaml")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)

    def test_files_theme(self):
        content = read("files/fmind.json")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", content))
        self.assertLessEqual(hex_codes, COLORS)

    def test_metatrader5_template(self):
        content = read("metatrader5/Fmind.tpl")
        self.assertIn("color_background=16777215", content)
        self.assertIn("color_foreground=2367776", content)
        self.readable("#202124", "#ffffff")

    def test_mutt_colors(self):
        content = read("mutt/fmind.muttrc")
        hex_codes = set(re.findall(r"color\d+\s+(#[0-9a-fA-F]{6})", content))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_microsoft_edge_theme(self):
        manifest = json.loads(read("microsoft-edge/manifest.json"))
        colors = manifest["theme"]["colors"]
        colors_hex = {k: (rgb(v) if isinstance(v, list) else v) for k, v in colors.items()}
        self.assertLessEqual(set(colors_hex.values()), COLORS)
        self.readable(colors_hex["tab_text"], colors_hex["toolbar"])

    def test_mousepad_scheme(self):
        content = read("mousepad/fmind.xml")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", content))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_vivado_theme(self):
        content = read("vivado/fmind.tcl")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", content))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_marp_theme(self):
        css = read("marp/fmind.css")
        hex_codes = set(re.findall(r"#[0-9a-fA-F]{6}", css))
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_git_colors(self):
        content = read("git/fmind.gitconfig")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#0d652d", "#ffffff")
        self.readable("#a50e0e", "#ffffff")

    def test_doom_emacs_theme(self):
        content = read("doom-emacs/doom-fmind-theme.el")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_total_commander_colors(self):
        content = read("total-commander/wincmd.ini")
        self.assertIn("BackColor=16777215", content)
        self.assertIn("ForeColor=2367776", content)
        self.readable("#202124", "#ffffff")

    def test_base16_scheme(self):
        data = yaml.safe_load(read("base16/fmind.yaml"))
        hex_codes = {"#" + v.lower() for k, v in data.items() if k.startswith("base")}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#" + data["base05"], "#" + data["base00"])

    def test_qt5_scheme(self):
        content = read("qt5/fmind.conf")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_coda_style(self):
        content = read("coda/Fmind.seestyle")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_colorls_theme(self):
        data = yaml.safe_load(read("colorls/fmind.yaml"))
        hex_codes = {v.lower() for v in data.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["dir"], "#ffffff")

    def test_aseprite_theme(self):
        content = read("aseprite/theme.xml")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_light_table_theme(self):
        css = read("light-table/fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_fl_studio_theme(self):
        content = read("fl-studio-21/Fmind.fltheme")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_vimium_style(self):
        css = read("vimium/fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_macdown_style(self):
        content = read("macdown/Fmind.style")
        hex_codes = {
            "#" + c.lower()
            for c in re.findall(
                r"(?m)^\s*(?:foreground|background|caret|selection|line-highlight):\s*([0-9a-fA-F]{6})",
                content,
            )
        }
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_nova_launcher_theme(self):
        data = json.loads(read("nova-launcher/fmind.json"))["colors"]
        hex_codes = {v.lower() for v in data.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["primary_text"], data["background"])

    def test_ida_pro_colors(self):
        content = read("ida/fmind.clr")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_tailwind_preset(self):
        content = read("tailwind/fmind.js")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_mattermost_theme(self):
        data = json.loads(read("mattermost/fmind.json"))
        hex_codes = {v.lower() for k, v in data.items() if v.startswith("#")}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["centerChannelColor"], data["centerChannelBg"])
        self.readable(data["sidebarText"], data["sidebarBg"])

    def test_aliucord_theme(self):
        data = json.loads(read("aliucord/fmind.json"))["color_palette"]
        hex_codes = {v.lower() for v in data.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["text_normal"], data["background_primary"])

    def test_xournalpp_palette(self):
        content = read("xournalpp/palette.ini")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_abap_theme(self):
        content = read("abap/fmind.xml")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_bbedit_colors(self):
        theme = plistlib.loads((ROOT / "bbedit/Fmind.bbColorScheme").read_bytes())
        hex_codes = {v.lower() for v in theme.values() if isinstance(v, str) and v.startswith("#")}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(theme["Foreground"], theme["Background"])

    def test_thunderbird_theme(self):
        manifest = json.loads(read("thunderbird/manifest.json"))
        colors = manifest["theme"]["colors"]
        hex_codes = {v.lower() for v in colors.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(colors["tab_text"], colors["tab_selected"])

    def test_logseq_style(self):
        content = read("logseq/custom.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_ulysses_style(self):
        data = json.loads(read("ulysses/Fmind.ulyssesstyle"))["colors"]
        hex_codes = {v.lower() for v in data.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["text"], data["background"])

    def test_jgrasp_colors(self):
        content = read("jgrasp/fmind.colors")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_kicad_theme(self):
        data = json.loads(read("kicad/fmind.json"))["colors"]["schematic"]
        hex_codes = {v.lower() for v in data.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["text"], data["background"])

    def test_ranger_colors(self):
        content = read("ranger/fmind.py")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_mailspring_theme(self):
        content = read("mailspring/ui-variables.less")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_ulauncher_theme(self):
        manifest = json.loads(read("ulauncher/manifest.json"))
        css = read("ulauncher/theme.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", manifest.get("matched_text_hl", "") + css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_ableton_live_skin(self):
        content = read("ableton-live/Fmind.ask")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_homer_style(self):
        content = read("homer/fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_wordpress_style(self):
        content = read("wordpress/fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_xchat_colors(self):
        content = read("xchat/pecolors.conf")
        hex_codes = {"#" + c.lower() for c in re.findall(r"=\s*([0-9a-fA-F]{6})", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_mixplorer_skin(self):
        content = read("mixplorer/Fmind.mit")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_texstudio_scheme(self):
        content = read("texstudio/fmind.txsCol")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_jdownloader2_theme(self):
        data = json.loads(read("jdownloader2/fmind.json"))["colors"]
        hex_codes = {v.lower() for v in data.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["foreground"], data["background"])

    def test_mindnode_theme(self):
        root = ET.fromstring(read("mindnode/fmind.mindnodetheme/contents.xml"))
        self.assertIsNotNone(root.find(".//key[.='backgroundColor']"))
        meta = plistlib.loads((ROOT / "mindnode/fmind.mindnodetheme/metadata.plist").read_bytes())
        self.assertEqual(meta["name"], "Fmind")
        self.readable("#202124", "#ffffff")

    def test_prism_theme(self):
        css = read("prism/prism-fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")
        self.readable("#174ea6", "#ffffff")

    def test_bashtop_theme(self):
        content = read("bashtop/fmind.theme")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_freecad_theme(self):
        css = read("freecad/Fmind.qss")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_adminer_theme(self):
        css = read("adminer/adminer.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_latex_theme(self):
        sty = read("latex/fmindtheme.sty")
        self.assertIn("\\definecolor{fmindbg}", sty)
        self.assertIn("\\definecolor{fmindfg}", sty)
        self.readable("#202124", "#ffffff")

    def test_plsql_developer_colors(self):
        content = read("plsql-developer/Fmind.ini")
        self.assertIn("KeywordsBkg=16777215", content)
        self.assertIn("EditorFontColor=2367776", content)
        self.readable("#202124", "#ffffff")

    def test_inkscape_palette(self):
        content = read("inkscape/fmind.gpl")
        self.assertTrue(content.startswith("GIMP Palette"))
        self.readable("#202124", "#ffffff")

    def test_textual_theme(self):
        css = read("textual/design.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_roam_research_theme(self):
        css = read("roam-research/fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_discourse_theme(self):
        meta = json.loads(read("discourse/about.json"))
        self.assertEqual(meta["name"], "Fmind Theme")
        scss = read("discourse/common/common.scss")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", scss)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_sumatra_pdf_theme(self):
        content = read("sumatra-pdf/Fmind.txt")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_youtube_music_desktop_theme(self):
        css = read("youtube-music-desktop/fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_macos_color_picker_palette(self):
        data = json.loads(read("macos-color-picker/palette.json"))["colors"]
        hex_codes = {v.lower() for v in data.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["Text"], data["Ground"])

    def test_plank_theme(self):
        content = read("plank/Fmind/dock.theme")
        self.assertIn("[PlankTheme]", content)
        self.assertIn("FillStartColor=255;;255;;255;;245", content)
        self.readable("#202124", "#ffffff")

    def test_quiver_theme(self):
        data = json.loads(read("quiver/Fmind.json"))
        hex_codes = {v.lower() for v in re.findall(r"#[0-9a-fA-F]{6}", read("quiver/Fmind.json"))}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["editor"]["textColor"], data["editor"]["backgroundColor"])

    def test_nextcloud_theme(self):
        css = read("nextcloud/theme.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_unreal_engine_theme(self):
        data = json.loads(read("unreal-engine/Fmind.json"))
        self.assertEqual(data["DisplayName"], "Fmind")
        self.readable("#202124", "#ffffff")

    def test_standard_notes_theme(self):
        ext = json.loads(read("standard-notes/ext.json"))
        self.assertEqual(ext["name"], "Fmind")
        css = read("standard-notes/dist/fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_quassel_theme(self):
        qss = read("quassel/Fmind.qss")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", qss)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_tabletop_simulator_theme(self):
        content = read("tabletop-simulator/fmind.txt")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_gitlab_style(self):
        css = read("gitlab/fmind.user.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_spicetify_theme(self):
        content = read("spicetify/color.ini")
        hex_codes = {f"#{c.lower()}" for c in re.findall(r"(?im)^\w[\w-]*\s*=\s*([0-9a-fA-F]{6})", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_tiddlywiki_theme(self):
        content = read("tiddlywiki/Fmind.tid")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_nylas_n1_theme(self):
        pkg = json.loads(read("nylas-n1/package.json"))
        self.assertEqual(pkg["name"], "fmind-theme")
        less = read("nylas-n1/index.less")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", less)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_bear_theme(self):
        data = json.loads(read("bear/fmind.bear"))
        self.assertEqual(data["name"], "Fmind")
        colors = data["colors"]
        hex_codes = {v.lower() for v in colors.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(colors["text"], colors["background"])

    def test_beyond_compare_theme(self):
        content = read("beyond-compare-4/BCColors-Fmind.xml")
        self.assertIn('BGColor Value="$FFFFFF"', content)
        self.readable("#202124", "#ffffff")

    def test_discord_bot_maker_theme(self):
        css = read("discordbotmaker/main.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_lightpaper_theme(self):
        content = read("lightpaper/Fmind.txt")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_javadoc_style(self):
        css = read("javadoc/stylesheet.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_spacemacs_theme(self):
        content = read("spacemacs/fmind-theme.el")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_florisboard_theme(self):
        data = json.loads(read("florisboard/fmind.json"))
        self.assertEqual(data["name"], "Fmind")
        sheet = data["stylesheet"]
        hex_codes = {v.lower() for v in sheet.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(sheet["foreground"], sheet["background"])

    def test_tty_colors(self):
        content = read("tty/fmind-tty.sh")
        hex_codes = {f"#{c.lower()}" for c in re.findall(r"\\e\]P[0-9a-fA-F]([0-9a-fA-F]{6})", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_google_calendar_style(self):
        css = read("google-calendar/fmind.user.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_openbox_theme(self):
        content = read("openbox/Fmind/openbox-3/themerc")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_editplus_theme(self):
        content = read("editplus/fmind.ini")
        self.assertIn("Background=16777215", content)
        self.assertIn("Foreground=2367776", content)
        self.readable("#202124", "#ffffff")

    def test_mkdocs_style(self):
        css = read("mkdocs/fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_krita_palette(self):
        content = read("krita/Fmind.colors")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_stackoverflow_style(self):
        css = read("stackoverflow/fmind.user.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_wolfram_notebooks_theme(self):
        content = read("wolfram-notebooks/Fmind.nb")
        self.assertIn("Background->RGBColor[1, 1, 1]", content)
        self.readable("#202124", "#ffffff")

    def test_minecraft_theme(self):
        meta = json.loads(read("minecraft/pack.mcmeta"))
        self.assertEqual(meta["pack"]["pack_format"], 15)
        self.readable("#202124", "#ffffff")

    def test_dircolors_theme(self):
        content = read("dircolors/.dircolors")
        self.assertIn("DIR 01;34", content)
        self.readable("#202124", "#ffffff")

    def test_coteditor_theme(self):
        data = json.loads(read("coteditor/Fmind.cottheme"))
        hex_codes = {v["color"].lower() for v in data.values() if "color" in v}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["text"]["color"], data["background"]["color"])

    def test_everythingtoolbar_theme(self):
        xaml = read("everythingtoolbar/Fmind.xaml")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", xaml)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_arduino_pro_ide_theme(self):
        data = json.loads(read("arduino-pro-ide/themes/fmind.json"))
        hex_codes = {v.lower() for v in data["colors"].values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["colors"]["editor.foreground"], data["colors"]["editor.background"])

    def test_p10k_oh_my_posh_theme(self):
        data = json.loads(read("p10k-oh-my-posh/powerlevel10k_fmind.omp.json"))
        hex_codes = {v.lower() for v in data["palette"].values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["palette"]["foreground"], data["palette"]["background"])

    def test_clone_hero_theme(self):
        content = read("clone-hero/Fmind.ini")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_gitkraken_theme(self):
        content = read("gitkraken/fmind-theme.jsonc")
        data = json.loads(content)
        root = data["themeValues"]["root"]
        hex_codes = {v.lower() for v in root.values() if v.startswith("#")}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(root["text-color"], root["app-bg"])

    def test_copyq_theme(self):
        content = read("copyq/fmind.ini")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_gimp_palette(self):
        content = read("gimp/Fmind.gpl")
        self.assertTrue(content.startswith("GIMP Palette"))
        self.readable("#202124", "#ffffff")

    def test_metaeditor_theme(self):
        content = read("metaeditor/metaeditor.ini")
        self.assertIn("Color0=16777215", content)
        self.assertIn("Color1=2367776", content)
        self.readable("#202124", "#ffffff")

    def test_ish_theme(self):
        data = json.loads(read("ish/Fmind.json"))["shared"]
        hex_codes = {c.lower() for c in data["colorPaletteOverrides"]}
        hex_codes.add(data["backgroundColor"].lower())
        hex_codes.add(data["foregroundColor"].lower())
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["foregroundColor"], data["backgroundColor"])

    def test_powershell_ise_theme(self):
        content = read("powershell-ise/fmind.ps1")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_i3lock_color_theme(self):
        content = read("i3lock-color/lock.sh")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_cava_theme(self):
        content = read("cava/config")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_sketch_palette(self):
        data = json.loads(read("sketch/fmind.sketchpalette"))
        self.assertEqual(len(data["colors"]), 5)
        self.readable("#202124", "#ffffff")

    def test_kdiff3_theme(self):
        content = read("kdiff3/kdiff3rc")
        self.assertIn("BgColor=255,255,255", content)
        self.assertIn("FgColor=32,33,36", content)
        self.readable("#202124", "#ffffff")

    def test_musicbee_skin(self):
        content = read("musicbee/Fmind.xml")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_scrivener_palette(self):
        content = read("scrivener/Fmind.pal")
        self.assertIn("Base(255,255,255)", content)
        self.assertIn("Text(32,33,36)", content)
        self.readable("#202124", "#ffffff")

    def test_liteide_theme(self):
        content = read("liteide/fmind.xml")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_homepage_theme(self):
        css = read("homepage-app/custom.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_ltspice_theme(self):
        content = read("ltspice/fmind-ltspice.ini")
        self.assertIn("Grid=16053233", content)
        self.assertIn("WaveColor0=10899479", content)
        self.readable("#202124", "#ffffff")

    def test_em_client_theme(self):
        xml = read("em-client/Fmind.emtheme")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", xml)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_nova_theme(self):
        ext = json.loads(read("nova/Fmind.novaextension/extension.json"))
        self.assertEqual(ext["name"], "Fmind")
        theme = json.loads(read("nova/Fmind.novaextension/Themes/fmind.json"))
        hex_codes = {v.lower() for v in theme["colors"].values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(theme["colors"]["foreground"], theme["colors"]["background"])

    def test_beamer_theme(self):
        sty = read("beamer/beamercolorthemefmind.sty")
        self.assertIn("\\definecolor{fmindbg}", sty)
        self.assertIn("\\definecolor{fmindfg}", sty)
        self.readable("#202124", "#ffffff")

    def test_pandoc_theme(self):
        theme = json.loads(read("pandoc/fmind.theme"))
        self.readable(theme["text-color"], theme["background-color"])
        for s in theme["text-styles"].values():
            if s.get("text-color"):
                self.assertIn(s["text-color"].lower(), COLORS)

    def test_delphi_theme(self):
        content = read("delphi/fmind.reg")
        self.assertIn('"ThemeName"="Fmind"', content)
        self.readable("#202124", "#ffffff")

    def test_django_admin_theme(self):
        css = read("django-admin/fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_kakoune_theme(self):
        kak = read("kakoune/colors/fmind.kak")
        self.assertIn('ground="rgb:ffffff"', kak)
        self.assertIn('text="rgb:202124"', kak)
        self.readable("#202124", "#ffffff")

    def test_albert_theme(self):
        qss = read("albert/Fmind.qss")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", qss)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_facebook_messenger_theme(self):
        css = read("facebook-messenger/fmind.user.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_couscous_theme(self):
        css = read("couscous/fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_renoise_theme(self):
        xrnc = read("renoise/fmind.xrnc")
        self.assertIn("<Main_Back>255,255,255</Main_Back>", xrnc)
        self.assertIn("<Main_Font>32,33,36</Main_Font>", xrnc)
        self.readable("#202124", "#ffffff")

    def test_ghostwriter_theme(self):
        theme = json.loads(read("ghostwriter/Fmind.json"))["light"]
        hex_codes = {v.lower() for v in theme.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(theme["foreground"], theme["background"])

    def test_papirus_folders_theme(self):
        sh = read("papirus-folders/fmind-papirus.sh")
        self.assertIn("papirus-folders -C blue", sh)
        self.readable("#202124", "#ffffff")

    def test_linear_theme(self):
        data = json.loads(read("linear/fmind.json"))
        self.assertEqual(data["name"], "Fmind")
        self.readable(data["text"], data["base"])

    def test_swiftui_theme(self):
        swift = read("swiftui/Fmind.swift")
        self.assertIn("public enum Fmind", swift)
        self.readable("#202124", "#ffffff")

    def test_audacity_theme(self):
        cfg = read("audacity/Fmind.cfg")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", cfg)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_node_console_theme(self):
        js = read("node-console/fmind.js")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", js)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_uptime_kuma_theme(self):
        css = read("uptime-kuma/theme.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_pywal_theme(self):
        data = json.loads(read("pywal/fmind.json"))
        hex_codes = {v.lower() for v in data["colors"].values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["special"]["foreground"], data["special"]["background"])

    def test_solidworks_theme(self):
        content = read("solidworks/fmind.sldreg")
        self.assertIn('"Background"=dword:00ffffff', content)
        self.readable("#202124", "#ffffff")

    def test_onecommander_theme(self):
        xaml = read("onecommander/Fmind.xaml")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", xaml)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_wing_theme(self):
        content = read("wing/fmind.py")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_cryptowatch_theme(self):
        content = read("cryptowatch/fmind.txt")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_ripcord_theme(self):
        data = json.loads(read("ripcord/fmind.json"))
        hex_codes = {v.lower() for v in data.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["text"], data["base"])

    def test_ditto_theme(self):
        content = read("ditto/Fmind.xml")
        self.assertIn("RGB(255, 255, 255)", content)
        self.assertIn("RGB(32, 33, 36)", content)
        self.readable("#202124", "#ffffff")

    def test_sidenotes_theme(self):
        data = json.loads(read("sidenotes/Fmind.sntheme"))["any"]
        self.assertEqual(data["systemAppearance"], "light")
        self.readable(data["notes"]["text"], data["notes"]["background"])

    def test_bemenu_theme(self):
        sh = read("bemenu/fmind.sh")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", sh)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_thelounge_theme(self):
        css = read("thelounge/fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_chatgpt_theme(self):
        css = read("chatgpt/fmind.user.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_mako_theme(self):
        content = read("mako/config")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_flarum_theme(self):
        css = read("flarum/fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_visual_basic_6_theme(self):
        content = read("visual-basic-6/fmind.ini")
        self.assertIn("Background=ffffff", content)
        self.assertIn("Foreground=202124", content)
        self.readable("#202124", "#ffffff")

    def test_nyxt_theme(self):
        content = read("nyxt/fmind.lisp")
        self.assertIn(':background-color "#ffffff"', content)
        self.assertIn(':on-background-color "#202124"', content)
        self.readable("#202124", "#ffffff")

    def test_joplin_theme(self):
        css = read("joplin/userchrome.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_unigram_theme(self):
        data = json.loads(read("unigram/Fmind.unigram-theme"))
        hex_codes = {v.lower() for v in data["colors"].values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["colors"]["windowForeground"], data["colors"]["windowBackground"])

    def test_prompt_theme(self):
        data = json.loads(read("prompt/fmind.json"))
        hex_codes = {c.lower() for c in data["colors"]}
        hex_codes.add(data["background"].lower())
        hex_codes.add(data["foreground"].lower())
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["foreground"], data["background"])

    def test_ncspot_theme(self):
        content = read("ncspot/config.toml")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_tower_theme(self):
        data = json.loads(read("tower/Fmind.towertheme"))
        bg = "#" + data["backgroundColor"]["hexValue"].lower()
        fg = "#" + data["textColor"]["hexValue"].lower()
        self.assertIn(bg, COLORS)
        self.assertIn(fg, COLORS)
        self.readable(fg, bg)

    def test_keypirinha_theme(self):
        content = read("keypirinha/fmind.ini")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_cider_theme(self):
        less = read("cider/index.less")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", less)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_dwarf_fortress_theme(self):
        content = read("dwarf-fortress/colors.txt")
        self.assertIn("[WHITE_R:32]", content)
        self.readable("#202124", "#ffffff")

    def test_google_search_theme(self):
        css = read("google-search/google-search.user.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_anne_pro_2_theme(self):
        data = json.loads(read("anne-pro-2/fmind.json"))["colors"]
        hex_codes = {v.lower() for v in data.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_apollo_theme(self):
        data = json.loads(read("apollo/fmind.json"))["theme"]
        hex_codes = {v.lower() for v in data.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["textColor"], data["backgroundColor"])

    def test_blockbench_theme(self):
        data = json.loads(read("blockbench/Fmind.bbtheme"))
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", data["css"])}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_limechat_theme(self):
        css = read("limechat/Fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_tint2_theme(self):
        content = read("tint2/tint2rc")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_fman_theme(self):
        css = read("fman/Theme.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_bobthefish_theme(self):
        content = read("bobthefish/fmind.fish")
        self.assertIn("function bobthefish_colors", content)
        self.readable("#202124", "#ffffff")

    def test_omarchy_theme(self):
        content = read("omarchy/hyprland.conf")
        self.assertIn("$background = rgb(ffffff)", content)
        self.readable("#202124", "#ffffff")

    def test_ngenuity_theme(self):
        data = json.loads(read("ngenuity/fmind.json"))["lighting"]
        hex_codes = {v.lower() for v in data.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["text"], data["primary"])

    def test_archive_of_our_own_theme(self):
        css = read("archive-of-our-own/fmind_ao3.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_abricotine_theme(self):
        css = read("abricotine/fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_coderunner_theme(self):
        content = read("coderunner/Fmind.tmTheme")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_calibre_palette(self):
        data = json.loads(read("calibre/fmind.calibre-palette"))["light"]["palette"]
        hex_codes = {v.lower() for v in data.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["Text"], data["Base"])

    def test_fig_theme(self):
        data = json.loads(read("fig/theme.json"))
        hex_codes = {v.lower() for k, v in data.items() if v.startswith("#")}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["foreground"], data["background"])

    def test_sequel_ace_theme(self):
        content = read("sequel-ace/fmind.spTheme")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_pi_coding_agent_theme(self):
        data = json.loads(read("pi-coding-agent/fmind.json"))["vars"]
        hex_codes = {v.lower() for v in data.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["foreground"], data["background"])

    def test_texshop_theme(self):
        plist = read("texshop/Fmind.plist")
        self.assertIn("background_R", plist)
        self.readable("#202124", "#ffffff")

    def test_duolingo_theme(self):
        css = read("duolingo/duolingo.user.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_tig_theme(self):
        content = read("tig/fmind.tigrc")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_codepen_theme(self):
        css = read("codepen/codepen.user.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_caprine_messenger_theme(self):
        css = read("caprine-messenger/custom.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_eza_theme(self):
        content = read("eza/theme.yml")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_postbox_theme(self):
        data = json.loads(read("postbox/Fmind.json"))
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", data[0]["body"])}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_vesktop_discord_theme(self):
        css = read("vesktop-discord/fmind.theme.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_blink_shell_theme(self):
        content = read("blink-shell/fmind.js")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_cli_visualizer_theme(self):
        content = read("cli-visualizer/fmind.vis")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_imageglass_theme(self):
        xml = read("imageglass/config.xml")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", xml)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_starship_powerline_preset_theme(self):
        content = read("starship-powerline-preset/starship.toml")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_exa_theme(self):
        content = read("exa/exa_colors.sh")
        self.assertIn("EXA_COLORS", content)
        self.readable("#202124", "#ffffff")

    def test_protonmail_theme(self):
        css = read("protonmail/fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_serenityos_theme(self):
        ini = read("serenityos/Fmind.ini")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", ini)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_snippetslab_theme(self):
        data = json.loads(read("snippetslab/fmind.json"))["interface"]
        hex_codes = {v.lower() for v in data.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["textColor"], data["backgroundColor"])

    def test_smartgit_theme(self):
        content = read("smartgit/fmind.theme")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", content)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_mantine_theme(self):
        data = json.loads(read("mantine/fmind.json"))["colors"]
        hex_codes = {c.lower() for group in data.values() for c in group}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_gajim_theme(self):
        css = read("gajim/fmind.css")
        hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable("#202124", "#ffffff")

    def test_noir_theme(self):
        data = json.loads(read("noir/fmind.json"))["colors"]
        hex_codes = {v.lower() for v in data.values()}
        self.assertLessEqual(hex_codes, COLORS)
        self.readable(data["text"], data["background"])

    def test_cli_developer_tools(self):
        rg = read("ripgrep/fmind.ripgreprc")
        self.assertIn("--colors=path:fg:17,78,166", rg)
        self.assertIn("--colors=match:bg:254,239,195", rg)

        grep = read("grep/fmind.sh")
        self.assertIn("GREP_COLORS=", grep)

        man = read("man-pages/fmind.sh")
        self.assertIn("LESS_TERMCAP_so=", man)

        nnn = read("nnn/fmind.sh")
        self.assertIn("NNN_COLORS=", nnn)

        tlrc = tomllib.loads(read("tlrc/fmind.toml"))
        self.assertEqual(tlrc["style"]["title"]["color"], "blue")

        lnav = json.loads(read("lnav/fmind.json"))
        styles = lnav["fmind-theme"]["theme"]["styles"]
        self.readable(styles["text"]["color"], styles["text"]["background-color"])
        self.readable(styles["keyword"]["color"], styles["text"]["background-color"])

        aerc = read("aerc/fmind")
        self.assertIn("statusline_default.bg = #f1f3f4", aerc)

        presenterm = yaml.safe_load(read("presenterm/fmind.yaml"))
        self.readable(presenterm["default"]["colors"]["foreground"], presenterm["default"]["colors"]["background"])

        tw = read("taskwarrior/fmind.theme")
        self.assertIn("color.header=color12", tw)

        gsv = ET.fromstring(read("gtksourceview/fmind.xml"))
        self.assertEqual(gsv.attrib["id"], "fmind")

        vis = read("vis/fmind.lua")
        self.assertIn('["black"] = "#202124"', vis)

        sp = json.loads(read("sandpack/fmind.json"))
        self.readable(sp["colors"]["base"], sp["colors"]["surface1"])

        peacock = json.loads(read("peacock-extension/fmind.json"))
        self.assertTrue(len(peacock["peacock.favoriteColors"]) >= 5)

    def test_web_css_styles(self):
        for app in (
            "dracula-css",
            "markdown-css",
            "macdown-css",
            "kagi",
            "deepseek",
            "forgejo",
            "miniflux",
            "astro-starlight",
            "tridactyl",
            "freshrss",
            "bookwyrm",
            "leetcode",
            "adventofcode",
            "libreddit",
            "nitter",
        ):
            css = read(f"{app}/fmind.css")
            hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
            self.assertLessEqual(hex_codes, COLORS, app)
            self.readable("#202124", "#ffffff", app)

    def test_batch_3_desktop_cli_tools(self):
        nb = read("newsboat/fmind.config")
        self.assertIn("color background white default", nb)

        tofi = read("tofi/fmind.ini")
        self.assertIn("text-color = #202124", tofi)

        sioyek = read("sioyek/fmind.config")
        self.assertIn("background_color #ffffff", sioyek)

        amfora = tomllib.loads(read("amfora/fmind.toml"))
        self.assertEqual(amfora["theme"]["background"], "#ffffff")

        kristall = ini("kristall/fmind.ini")
        self.assertEqual(kristall["theme"]["background"], "#ffffff")

        goaccess = read("go-access/fmind.conf")
        self.assertIn("color_scheme 0", goaccess)

        castero = read("castero/fmind.conf")
        self.assertIn("color_background = white", castero)

        tut = ini("tut/fmind.ini")
        self.assertEqual(tut["theme"]["background"].strip('"'), "#ffffff")

        fluxbox = read("fluxbox/fmind")
        self.assertIn("toolbar.color: #ffffff", fluxbox)

        tabbed = read("suckless-tabbed/fmind.h")
        self.assertIn('"#202124"', tabbed)

        yakuake = ini("yakuake/fmind.skin")
        self.assertEqual(yakuake["Skin"]["name"], "Fmind")

        musikcube = json.loads(read("musikcube/fmind.json"))
        self.assertEqual(musikcube["colors"]["background"], "#ffffff")

        leftwm = read("leftwm/theme.ron")
        self.assertIn('"#174ea6"', leftwm)

        alphai = json.loads(read("alphai-tui/fmind.json"))
        self.assertEqual(alphai["background"], "#ffffff")

        openscad = json.loads(read("openscad/fmind.json"))
        self.assertEqual(openscad["background"], "#ffffff")

        speedcrunch = json.loads(read("speedcrunch/fmind.json"))
        self.assertEqual(speedcrunch["background"], "#ffffff")

        fw = ini("focuswriter/fmind.fwt")
        self.assertEqual(fw["General"]["background_color"], "#ffffff")

        nw = ini("novel-writer/fmind.conf")
        self.assertEqual(nw["Colors"]["background"], "#ffffff")

        tw = read("texworks/fmind.xml")
        self.assertIn('color="#174ea6"', tw)

        r = read("r/fmind.R")
        self.assertIn('black = "#202124"', r)

        gg = read("ggplot2/fmind.R")
        self.assertIn("theme_fmind", gg)

    def test_batch_4_web_and_app_tools(self):
        for app in (
            "jellyfin",
            "freetube",
            "funkwhale",
            "peertube",
            "stirling-pdf",
            "notesnook",
            "whatsapp-web",
            "facebook",
            "tumblr",
            "bandcamp",
            "codeforces",
            "keybr",
            "todoist",
            "ldoc",
        ):
            css = read(f"{app}/fmind.css")
            hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
            self.assertLessEqual(hex_codes, COLORS, app)
            self.readable("#202124", "#ffffff", app)

        revolt = json.loads(read("revolt/fmind.json"))
        self.readable(revolt["variables"]["foreground"], revolt["variables"]["background"])

        chatterino = json.loads(read("chatterino/fmind.json"))
        self.readable(chatterino["colors"]["foreground"], chatterino["colors"]["background"])

        misskey = json.loads(read("misskey/fmind.json"))
        self.readable(misskey["props"]["fg"], misskey["props"]["bg"])

        ha = yaml.safe_load(read("home-assistant/fmind.yaml"))["fmind"]
        self.readable(ha["primary-text-color"], ha["primary-background-color"])

        sniff = tomllib.loads(read("sniffnet/fmind.toml"))["palette"]
        self.readable(sniff["text_body"], "#ffffff")

        postman = json.loads(read("postman/fmind.json"))["colors"]
        self.readable(postman["text"], postman["background"])

    def test_batch_5_desktop_security_tools(self):
        for app in ("signal-desktop", "beeper", "dash", "readwise-reader"):
            css = read(f"{app}/fmind.css")
            hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
            self.assertLessEqual(hex_codes, COLORS, app)
            self.readable("#202124", "#ffffff", app)

        for app in ("tableplus", "docker", "ueli", "passky", "runjs", "cadzinho", "cutter"):
            doc = json.loads(read(f"{app}/fmind.json"))
            self.assertTrue(len(doc) > 0, app)

        anytype = dict(re.findall(r"(--[\w-]+):\s*(#[\da-f]{6})", read("anytype/custom.css")))
        for text in ("primary", "secondary", "tertiary"):
            for surface in ("primary", "secondary", "tertiary"):
                self.readable(anytype[f"--color-text-{text}"], anytype[f"--color-bg-{surface}"])
            self.readable(anytype[f"--color-text-{text}"], anytype["--color-system-selection"])
            self.readable(anytype[f"--color-text-{text}-inversion"], anytype["--color-bg-primary-inversion"])

        self.assertIn("[Fmind]", read("securecrt/fmind.ini"))
        self.assertIn('<Theme Name="Fmind">', read("mremoteng/fmind.xml"))
        self.assertIn("APT::Color", read("apt/fmind.conf"))
        self.assertIn("[Colors]", read("x64dbg/fmind.ini"))
        self.assertIn("[Colors]", read("xdbg/fmind.ini"))
        self.assertIn('"name": "Fmind"', read("forklift/fmind.flcolors"))
        self.assertIn('"textColor": "#202124"', read("marta/fmind.kana"))
        self.assertIn("[Theme]", read("directory-opus/fmind.dps"))

    def test_batch_6_games_and_tools(self):
        for app in (
            "heroic-games-launcher",
            "new-tabs",
            "infinity-for-reddit",
            "vital",
            "revolution-irc",
            "polymc",
            "psychopy",
            "harpy-for-twitter",
            "color-slurp",
        ):
            fname = (
                "theme.json"
                if app == "polymc"
                else (
                    "fmind.vitalskin"
                    if app == "vital"
                    else ("fmind.irctheme" if app == "revolution-irc" else "fmind.json")
                )
            )
            doc = json.loads(read(f"{app}/{fname}"))
            self.assertTrue(len(doc) > 0, app)

        for app in ("visual-spigot", "flowlab", "lichess", "btcpay-server", "gemini"):
            fname = "fmind.user.css" if app == "lichess" else "fmind.css"
            css = read(f"{app}/{fname}")
            hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
            self.assertLessEqual(hex_codes, COLORS, app)
            self.readable("#202124", "#ffffff", app)

        self.assertIn("[Plymouth Theme]", read("plymouth/fmind.plymouth"))
        self.assertIn("<plist", read("textastic/fmind.tmTheme"))
        self.assertIn("fontforge.View.Background", read("fontforge/fmind.txt"))
        self.assertIn("name: Fmind", read("drafts/fmind.yml"))
        self.assertIn("theme\n{", read("nilesoft-shell/fmind.nss"))
        self.assertIn("style/color_scheme", read("rime/fmind.yaml"))
        self.assertIn("$brand-primary", read("vortex-mod-manager/fmind.scss"))

    def test_batch_7_media_web_tools(self):
        for app in (
            "omglol",
            "campfire",
            "itfy",
            "kanbanflow",
            "yunohost",
            "wp",
            "subsonic",
            "replugged",
            "jabref",
            "auto-ao3-app",
        ):
            fname = "fmind.user.css" if app in ("itfy", "auto-ao3-app") else "fmind.css"
            css = read(f"{app}/{fname}")
            hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
            self.assertLessEqual(hex_codes, COLORS, app)
            self.readable("#202124", "#ffffff", app)

        for app in ("thumb-key", "dyalog", "kurozora", "fedilab"):
            doc = json.loads(read(f"{app}/fmind.json"))
            self.assertTrue(len(doc) > 0, app)

        self.assertIn("<color-scheme", read("labplot/fmind.xml"))
        self.assertIn("BACKGROUND=#ffffff", read("m8/fmind.m8t"))
        self.assertIn("[Theme]", read("snappy-driver-installer/fmind.txt"))
        self.assertIn("Background=#ffffff", read("acs/fmind.col"))
        self.assertIn("QWidget", read("makehuman/fmind.qss"))
        self.assertIn("[Theme]", read("lcd-smartie/fmind.ini"))
        self.assertIn("<plist", read("newterm2/fmind.plist"))

    def test_batch_8_dashboards_and_apps(self):
        for app in ("gitroll", "unraid", "dankmaterialshell", "librenms", "kali-browser"):
            fname = "fmind.user.css" if app == "librenms" else "fmind.css"
            css = read(f"{app}/{fname}")
            hex_codes = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", css)}
            self.assertLessEqual(hex_codes, COLORS, app)
            self.readable("#202124", "#ffffff", app)

        for app in ("superset", "t3code", "rackula", "trudido", "neiki-editor", "stationview", "neiki-page-editor"):
            doc = json.loads(read(f"{app}/fmind.json"))
            self.assertTrue(len(doc) > 0, app)

        self.assertIn("[Colors]", read("adiirc/fmind.ini"))
        self.assertIn("theme: light", read("evidence/fmind.yaml"))
        self.assertIn("theme:", read("hermes-agent/fmind.yaml"))
        self.assertIn('"name":"Fmind"', read("bettercanvas/fmind.txt"))
        self.assertIn("windowBackground: #ffffff", read("telegram-macos/fmind.palette"))
        self.assertIn("windowBackground: #ffffff", read("telegram-x/fmind.tgx-theme"))
        self.assertIn("[Theme]", read("snappy-driver-installer-origin/fmind.txt"))
        self.assertIn("[theme]", read("wiremix/fmind.toml"))
