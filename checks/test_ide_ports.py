"""Native IDE profile boundaries and readable syntax on editor overlays."""

import configparser
import json
import re
import unittest
import xml.etree.ElementTree as ET

import tinycss2
from test_theme import PALETTE, ROOT, contrast

COLORS = set(PALETTE["official"] + PALETTE["custom"])
# These editor ports use pale overlays, never the terminal's saturated label fill.
SURFACES = {PALETTE["ground"], *(PALETTE["surfaces"][key] for key in ("line", "selection", "plus", "minus", "change"))}


def rgb(channels):
    return "#" + "".join(f"{int(value):02x}" for value in channels)


class IdePortTests(unittest.TestCase):
    def readable(self, foreground, background, label):
        self.assertIn(foreground, COLORS, label)
        self.assertIn(background, COLORS, label)
        self.assertGreaterEqual(contrast(foreground, background), 4.5, label)

    def test_netbeans_syntax_and_annotations(self):
        files = list((ROOT / "netbeans/config/Editors").rglob("*.xml"))
        self.assertEqual(len(files), 30)
        self.assertEqual(sum(p.name.endswith("tokenColorings.xml") for p in files), 28)
        total = 0
        for path in files:
            root = ET.parse(path).getroot()
            self.assertEqual(root.tag, "fontscolors")
            styles = root.findall("fontcolor")
            self.assertEqual(len({s.get("name") for s in styles}), len(styles), str(path))
            total += len(styles)
            for style in styles:
                label = str(path.relative_to(ROOT)) + ": " + style.get("name")
                for key in ("foreColor", "bgColor", "underline", "waveUnderlined", "strikeThrough"):
                    if key in style.attrib:
                        self.assertRegex(style.get(key), r"^ff[0-9a-f]{6}$", label)
                        self.assertIn("#" + style.get(key)[2:], COLORS, label)
                fg = "#" + style.get("foreColor", "ff202124")[2:]
                bg = "#" + style.get("bgColor", "ffffffff")[2:]
                self.readable(fg, bg, label)
                for surface in SURFACES:
                    self.readable(fg, surface, label)
        self.assertEqual(total, 549)
        shared = ROOT / "netbeans/config/Editors/FontsColors/Fmind"
        default = ET.parse(next(shared.glob("*tokenColorings.xml"))).find('./fontcolor[@name="default"]')
        self.assertEqual(default.get("bgColor"), "ffffffff")
        self.assertEqual(default.find("font").get("name"), "Google Sans Code")

    def test_netbeans_import_contains_only_color_settings(self):
        config = ROOT / "netbeans/config"
        attrs = ET.parse(config / ".nbattrs").getroot()
        self.assertEqual(len(attrs), 1)
        self.assertEqual(attrs[0].get("name"), "Editors")
        self.assertEqual(attrs[0][0].attrib, {"name": "currentFontColorProfile", "stringvalue": "Fmind"})
        for path in (config / "Editors").rglob(".nbattrs"):
            for file in ET.parse(path).getroot():
                self.assertTrue((path.parent / file.get("name")).is_file())
                self.assertEqual(len(file), 1)
                self.assertEqual(file[0].get("name"), "nbeditor-settings-ColoringType")
                self.assertIn(file[0].get("stringvalue"), ("token", "highlight", "annotation"))
        self.assertFalse((ROOT / "netbeans/build.info").exists())
        self.assertEqual((ROOT / "netbeans/enabledItems.info").read_text().strip(), "Fonts & ColorsFmind")

    def test_codeblocks_lexers_and_style_pairs(self):
        root = ET.parse(ROOT / "codeblocks/fmind.conf").getroot()
        self.assertEqual(root.tag, "CodeBlocksConfig")
        self.assertEqual([e.tag for e in root], ["editor"])
        theme = root.find("editor/colour_sets/fmind")
        self.assertEqual(theme.findtext("NAME/str"), "Fmind")
        languages = [e for e in theme if e.tag != "NAME"]
        self.assertEqual(len(languages), 62)
        self.assertEqual(len({e.tag for e in languages}), 62)
        count = 0
        for language in languages:
            styles = [e for e in language if e.tag != "NAME"]
            self.assertEqual([s.tag for s in styles], [f"style{i}" for i in range(len(styles))])
            names = [s.findtext("NAME/str") for s in styles]
            self.assertEqual(len(names), len(set(names)))
            self.assertTrue({"Selection", "Active line", "Matching brace highlight"} <= set(names))
            for style in styles:
                label = language.tag + ": " + style.findtext("NAME/str")
                fg = rgb(style.find("FORE/colour").get(c) for c in "rgb")
                bg = rgb(style.find("BACK/colour").get(c) for c in "rgb")
                self.readable(fg, bg, label)
                for surface in SURFACES:
                    self.readable(fg, surface, label)
            count += len(styles)
        self.assertEqual(count, 1324)
        html = theme.find("htmlphpaspjs")
        names = {s.findtext("NAME/str") for s in html if s.tag != "NAME"}
        self.assertIn("HTML Default", names)
        self.assertNotIn("Default", names)

    def test_dev_cpp_colorref_encoding_and_states(self):
        config = configparser.ConfigParser(interpolation=None)
        config.optionxform = str
        config.read(ROOT / "dev-cpp/Fmind.syntax")
        self.assertEqual(config.sections(), ["Editor.Custom"])
        values = config["Editor.Custom"]
        self.assertEqual(len(values), 20)
        syntax = []
        for name, value in values.items():
            parts = [p.strip() for p in value.split(",")]
            self.assertIn(len(parts), (2, 5))
            colors = []
            for encoded in parts[:2]:
                self.assertRegex(encoded, r"^\$00[0-9a-f]{6}$")
                colors.append("#" + encoded[7:9] + encoded[5:7] + encoded[3:5])
            self.readable(*colors, name)
            if len(parts) == 5:
                syntax.append(name)
                self.assertLessEqual(set(parts[2:]), {"0", "1"})
                for surface in SURFACES:
                    self.readable(colors[0], surface, name)
        self.assertEqual(len(syntax), 14)
        self.assertTrue({"String", "Comment", "Number", "Reserved Word"} <= set(syntax))

    def test_eclipse_roles_and_native_preferences(self):
        theme = ET.parse(ROOT / "eclipse/fmind.xml").getroot()
        self.assertEqual(theme.get("name"), "Fmind")
        roles = {e.tag: e.get("color") for e in theme}
        self.assertEqual(len(roles), 47)
        self.assertLessEqual(set(roles.values()), COLORS)
        for role in ("keyword", "string", "number", "singleLineComment", "class", "foreground", "lineNumber"):
            for surface in SURFACES:
                self.readable(roles[role], surface, role)
        self.readable(roles["selectionForeground"], roles["selectionBackground"], "selection")
        entries = [
            line.split("=", 1)
            for line in (ROOT / "eclipse/fmind.epf").read_text().splitlines()
            if line and not line.startswith("#")
        ]
        prefs = dict(entries)
        self.assertEqual(len(entries), len(prefs))
        self.assertEqual(prefs.pop("file_export_version"), "3.0")
        self.assertEqual(len(prefs), 382)
        self.assertEqual(len({key.split("/")[2] for key in prefs}), 6)
        for key, value in prefs.items():
            self.assertTrue(key.startswith("/instance/"), key)
            if re.fullmatch(r"\d+,\d+,\d+", value):
                self.assertIn(rgb(value.split(",")), COLORS, key)
            elif key.endswith("SystemDefault"):
                self.assertEqual(value, "false", key)
        self.assertEqual(prefs["/instance/org.eclipse.jdt.ui/java_keyword"], "23,78,166")
        self.assertEqual(prefs["/instance/org.eclipse.cdt.ui/c_string"], "13,101,45")
        self.assertEqual(prefs["/instance/org.python.pydev/NUMBER_COLOR"], "147,73,0")

    def test_atom_package_and_public_syntax_variables(self):
        package = json.loads((ROOT / "atom/package.json").read_text())
        self.assertEqual(package["name"], "fmind-syntax")
        self.assertEqual(package["theme"], "syntax")
        variables = (ROOT / "atom/styles/syntax-variables.less").read_text()
        colors = (ROOT / "atom/styles/colors.less").read_text()
        values = dict(re.findall(r"(@[\w-]+):\s*([^;]+);", colors + variables))

        def resolve(name):
            seen = set()
            while name.startswith("@"):
                self.assertNotIn(name, seen)
                seen.add(name)
                name = values[name]
            return name

        for name in values:
            self.assertIn(resolve(name), COLORS, name)
        for role in ("text", "gutter-text", "color-variable", "color-constant", "color-function", "color-class"):
            name = "@syntax-" + role + ("-color" if role in ("text", "gutter-text") else "")
            for bg in ("@syntax-background-color", "@syntax-selection-color"):
                self.readable(resolve(name), resolve(bg), name)
        self.assertEqual(resolve("@syntax-background-color"), "#ffffff")
        self.assertEqual(resolve("@syntax-color-added"), "#0d652d")

    def test_brackets_native_css_and_light_package(self):
        package = json.loads((ROOT / "brackets/package.json").read_text())
        self.assertIs(package["theme"]["dark"], False)
        source = (ROOT / "brackets" / package["theme"]["file"]).read_text()
        selectors = []
        for rule in tinycss2.parse_stylesheet(source, skip_comments=True, skip_whitespace=True):
            self.assertEqual(rule.type, "qualified-rule")
            selector = tinycss2.serialize(rule.prelude).strip()
            selectors.append(selector)
            declarations = tinycss2.parse_declaration_list(rule.content, skip_comments=True, skip_whitespace=True)
            self.assertTrue(all(d.type == "declaration" for d in declarations), selector)
            values = {d.name: tinycss2.serialize(d.value).strip() for d in declarations}
            if "color" in values:
                self.readable(values["color"], values.get("background", "#ffffff"), selector)
                for surface in SURFACES:
                    self.readable(values["color"], surface, selector)
        for required in (".CodeMirror .cm-comment", ".CodeMirror .cm-error", ".CodeMirror .cm-positive"):
            self.assertIn(required, selectors)
