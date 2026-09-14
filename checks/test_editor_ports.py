"""Native editor contracts, including lexer IDs, light UI pairs and diff surfaces."""

import ast
import configparser
import plistlib
import re
import unittest
import xml.etree.ElementTree as ET

import tinycss2
from test_theme import PALETTE, ROOT, contrast

COLORS = set(PALETTE["official"] + PALETTE["custom"])


def ini(path):
    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str
    parser.read(ROOT / path)
    return parser


class EditorPortTests(unittest.TestCase):
    def readable(self, fg, bg, label=""):
        self.assertIn(fg, COLORS, label)
        self.assertIn(bg, COLORS, label)
        self.assertGreaterEqual(contrast(fg, bg), 4.5, label)

    def test_notepad_lexer_ids_and_style_backgrounds(self):
        root = ET.parse(ROOT / "notepad-plus-plus/fmind.xml").getroot()
        self.assertEqual(root.tag, "NotepadPlus")
        lexers = root.findall("./LexerStyles/LexerType")
        self.assertEqual(len(lexers), 60)
        self.assertEqual(len({lexer.get("name") for lexer in lexers}), len(lexers))
        self.assertEqual(len(root.findall(".//WordsStyle")), 842)
        for lexer in lexers:
            styles = lexer.findall("WordsStyle")
            self.assertEqual(len({int(s.get("styleID")) for s in styles}), len(styles), lexer.get("name"))
            for style in styles:
                fg = "#" + style.get("fgColor").lower()
                bg = "#" + style.get("bgColor").lower()
                self.readable(fg, bg, lexer.get("name") + ": " + style.get("name"))
                self.assertEqual(style.get("colorStyle"), "3")
                self.assertIn(style.get("fontStyle"), ("0", "1"))
                for surface in ("selection", "line", "plus", "minus", "change"):
                    self.readable(fg, PALETTE["surfaces"][surface], style.get("name"))
        python = {int(s.get("styleID")): s for s in root.findall('./LexerStyles/LexerType[@name="python"]/WordsStyle')}
        self.assertEqual(python[1].get("fgColor"), "595D62")
        self.assertEqual(python[2].get("fgColor"), "934900")
        self.assertEqual(python[5].get("fgColor"), "174EA6")
        self.assertEqual(python[6].get("fgColor"), "0D652D")

    def test_notepad_global_highlights_and_tabs(self):
        root = ET.parse(ROOT / "notepad-plus-plus/fmind.xml").getroot()
        styles = {e.get("name"): e.attrib for e in root.findall("./GlobalStyles/WidgetStyle")}
        backgrounds = {"#" + e["bgColor"].lower() for e in styles.values() if "bgColor" in e}
        for name in ("Default Style", "Selected text colour", "Active tab text", "Inactive tabs", "Line number margin"):
            self.readable("#" + styles[name]["fgColor"].lower(), "#" + styles[name]["bgColor"].lower(), name)
        for name, style in styles.items():
            if name.startswith(("Mark Style", "Tab color")):
                self.readable(PALETTE["text"], "#" + style["bgColor"].lower(), name)
        for fg in PALETTE["roles"].values():
            for bg in backgrounds:
                self.readable(fg, bg, "Notepad++ syntax overlay")

    def test_qtcreator_native_color_roles_and_ui_pairs(self):
        theme = ini("qtcreator/fmind.creatortheme")
        self.assertEqual(theme["General"]["ThemeName"], "Fmind")
        self.assertNotIn("Includes", theme["General"])
        self.assertEqual(theme["Flags"]["DarkUserInterface"], "false")
        self.assertEqual(theme["Flags"]["ApplyThemePaletteGlobally"], "true")
        self.assertEqual(len(theme["Colors"]), 441)
        colors = {}
        for key, value in theme["Colors"].items():
            self.assertRegex(value, r"^ff[0-9a-f]{6}$", key)
            colors[key] = "#" + value[2:]
            self.assertIn(colors[key], COLORS, key)
        self.assertEqual([colors[f"TerminalAnsi{i}"] for i in range(16)], list(PALETTE["ansi"].values()))
        # Qt's Foreground tokens are control fills, despite their names.
        for text in ("Default", "Muted", "Subtle"):
            for surface in ("Default", "Muted", "Subtle"):
                self.readable(colors["Token_Text_" + text], colors["Token_Foreground_" + surface], text)
        for suffix in ("", "Disabled"):
            for fg, bg in (
                ("PaletteWindowText", "PaletteWindow"),
                ("PaletteText", "PaletteBase"),
                ("PaletteButtonText", "PaletteButton"),
                ("PaletteToolTipText", "PaletteToolTipBase"),
                ("PaletteHighlightedText", "PaletteHighlight"),
                ("PalettePlaceholderText", "PaletteBase"),
            ):
                self.readable(colors[fg + suffix], colors[bg + suffix], fg + suffix)
        for fg, bg in (
            ("Token_Text_Default", "Token_Background_Default"),
            ("Token_Text_On_Accent", "Token_Accent_Default"),
            ("InfoBarText", "InfoBarBackground"),
            ("DStextColor", "DScontrolBackground"),
            ("DStextSelectedTextColor", "DStextSelectionColor"),
            ("DStextColorDisabled", "DScontrolBackgroundDisabled"),
            ("DStableHeaderText", "DStableHeaderBackground"),
            ("DStitleBarText", "DSdockWidgetTitleBar"),
            ("DStoolTipText", "DStoolTipBackground"),
            ("TerminalForeground", "TerminalSelection"),
            ("TerminalForeground", "TerminalBackground"),
        ):
            self.readable(colors[fg], colors[bg], fg)
        for state in ("Active", "Inactive", "Focus"):
            self.readable(colors[f"DStab{state}Text"], colors[f"DStab{state}Background"], state)
        for state in ("", "Hover", "Selected"):
            self.readable(colors["DSnavigatorText" + state], colors["DSnavigatorItemBackground" + state], state)
        for key, fg in colors.items():
            if key.startswith(("OutputPanes_", "Debugger_WatchItem_", "VcsBase_")) and not "Background" in key:
                self.readable(fg, colors["PaletteBase"], key)

    def test_qtcreator_editor_syntax_and_diffs(self):
        root = ET.parse(ROOT / "qtcreator/fmind.xml").getroot()
        self.assertEqual(root.attrib, {"version": "1.0", "name": "Fmind"})
        styles = {s.get("name"): s.attrib for s in root.findall("style")}
        self.assertEqual(len(styles), 66)
        surfaces = [s["background"] for s in styles.values() if "background" in s]
        for name, style in styles.items():
            if name == "VisualWhitespace":
                continue
            for bg in surfaces:
                self.readable(style["foreground"], bg, name)
        for name in ("Error", "ErrorContext", "Warning", "WarningContext"):
            self.assertIn(styles[name]["underlineColor"], COLORS)
            self.assertIn(styles[name]["underlineStyle"], ("WaveUnderline", "DotLine"))

    def test_spyder_complete_custom_scheme_values(self):
        theme = ini("spyder/fmind.ini")["appearance"]
        self.assertEqual(theme["custom-0/name"], "Fmind")
        self.assertNotIn("custom_names", theme)
        self.assertNotIn("names", theme)
        surfaces = {
            key: theme["custom-0/" + key]
            for key in (
                "background",
                "currentline",
                "currentcell",
                "occurrence",
                "sideareas",
                "matched_p",
                "unmatched_p",
            )
        }
        syntax = ("normal", "keyword", "magic", "builtin", "definition", "comment", "string", "number", "instance")
        self.assertEqual(len(theme), len(surfaces) + len(syntax) + 2)
        for key in syntax:
            fg, bold, italic = ast.literal_eval(theme["custom-0/" + key])
            self.assertIsInstance(bold, bool)
            self.assertIs(italic, False)
            for bg in surfaces.values():
                self.readable(fg, bg, key)
        self.readable(theme["custom-0/ctrlclick"], surfaces["background"])

    def test_textmate_identity_syntax_and_overlays(self):
        theme = plistlib.loads((ROOT / "textmate/fmind.tmTheme").read_bytes())
        self.assertEqual(theme["semanticClass"], "theme.light.fmind")
        self.assertRegex(theme["uuid"], r"^[A-F0-9]{8}(?:-[A-F0-9]{4}){3}-[A-F0-9]{12}$")
        base = theme["settings"][0]["settings"]
        self.readable(base["foreground"], base["background"])
        self.readable(base["gutterForeground"], base["gutterBackground"])
        self.readable(base["selectionForeground"], base["selection"])
        for rule in theme["settings"][1:]:
            fg = rule["settings"]["foreground"]
            for bg in (base["background"], base["selection"], base["lineHighlight"], base["findHighlight"]):
                self.readable(fg, bg, rule["scope"])
            if "background" in rule["settings"]:
                self.readable(fg, rule["settings"]["background"], rule["scope"])

    def test_rstudio_supported_css_selectors_and_surfaces(self):
        source = (ROOT / "rstudio/fmind.rstheme").read_text()
        self.assertIn("/* rs-theme-is-dark: FALSE */", source)
        self.assertIn("/* rs-theme-name: Fmind */", source)
        rules = {}
        for rule in tinycss2.parse_stylesheet(source, skip_comments=True, skip_whitespace=True):
            self.assertEqual(rule.type, "qualified-rule")
            selectors = tinycss2.serialize(rule.prelude).strip().split(", ")
            declarations = {}
            for item in tinycss2.parse_declaration_list(rule.content, skip_comments=True, skip_whitespace=True):
                self.assertEqual(item.type, "declaration")
                declarations[item.name] = tinycss2.serialize(item.value).strip()
            for selector in selectors:
                rules.setdefault(selector, {}).update(declarations)
        self.assertEqual(rules[".ace_editor"]["background-color"], "#ffffff")
        for fg, bg in (
            (".ace_editor", ".ace_editor"),
            (".ace_gutter", ".ace_gutter"),
            (".rstheme_selected", ".rstheme_selected"),
            (".ace_autocomplete .ace_completion-meta", ".ace_autocomplete"),
        ):
            self.readable(rules[fg]["color"], rules[bg]["background-color"], fg)
        surfaces = [
            rules[key]["background-color"]
            for key in (
                ".ace_editor",
                ".ace_marker-layer .ace_selection",
                ".ace_marker-layer .ace_active-line",
                ".ace_marker-layer .ace_active-debug-line",
                ".ace_marker-layer .ace_find_line",
                ".ace_diff.ace_deleted",
            )
        ]
        for selector, fields in rules.items():
            if selector.startswith(".ace_") and "color" in fields:
                for bg in surfaces:
                    self.readable(fields["color"], bg, selector)
        self.assertEqual(
            [rules[f".terminal .xtermColor{i}"]["color"] for i in range(16)], list(PALETTE["ansi"].values())
        )
        for color in re.findall(r"#[a-f0-9]{6}", source):
            self.assertIn(color, COLORS)
