"""GTK package imports, native RC states and explicitly paired CSS surfaces."""

import configparser
import re
import unittest

import tinycss2
from test_theme import ROOT, contrast

GTK = ROOT / "gtk"


def stylesheet(path):
    """Reject malformed CSS, retaining native at-rules and declaration order."""
    rules = tinycss2.parse_stylesheet(path.read_text(), skip_comments=True, skip_whitespace=True)
    for rule in rules:
        if rule.type not in {"qualified-rule", "at-rule"}:
            raise ValueError(f"{path.name}: {rule.type}")
        if rule.type == "qualified-rule":
            for item in tinycss2.parse_declaration_list(rule.content, skip_comments=True, skip_whitespace=True):
                if item.type != "declaration":
                    raise ValueError(f"{path.name}: {item.type}")
    return rules


def css_values(rule):
    return {
        item.name: tinycss2.serialize(item.value).strip()
        for item in tinycss2.parse_declaration_list(rule.content, skip_comments=True, skip_whitespace=True)
    }


class GtkPortTests(unittest.TestCase):
    def test_native_entry_points_and_import_closure(self):
        index = configparser.ConfigParser()
        index.read(GTK / "index.theme")
        self.assertEqual(index["X-GNOME-Metatheme"]["GtkTheme"], "Fmind")
        self.assertEqual(index["X-GNOME-Metatheme"]["MetacityTheme"], "Fmind")
        expected_resources = {
            "gtk-3.0": "resource:///org/gtk/libgtk/theme/Adwaita/gtk.css",
            "gtk-4.0": "resource:///org/gtk/libgtk/theme/Default/gtk.css",
        }
        for version, resource in expected_resources.items():
            imports = [
                tinycss2.serialize(r.prelude).strip()
                for r in stylesheet(GTK / version / "gtk.css")
                if r.type == "at-rule" and r.lower_at_keyword == "import"
            ]
            self.assertEqual(imports, [f'url("{resource}")', 'url("../common.css")'])
            dark = stylesheet(GTK / version / "gtk-dark.css")
            self.assertEqual(len(dark), 1)
            self.assertEqual(dark[0].lower_at_keyword, "import")
            self.assertEqual(tinycss2.serialize(dark[0].prelude).strip(), 'url("gtk.css")')
        for path in GTK.rglob("*.css"):
            for target in re.findall(r'@import url\("([^"\n]+)"\)', path.read_text()):
                if path == GTK / "cinnamon/cinnamon.css" and target == "/usr/share/cinnamon/theme/cinnamon.css":
                    # Cinnamon supplies the native layout; its runtime is optional in the offline gate.
                    continue
                if not target.startswith("resource:"):
                    self.assertTrue((path.parent / target).is_file(), (path, target))

    def test_css_surface_pairs_and_gradient_resets(self):
        for path in GTK.rglob("*.css"):
            for rule in stylesheet(path):
                if rule.type != "qualified-rule":
                    continue
                values = css_values(rule)
                fg, bg = values.get("color", ""), values.get("background-color", "")
                if fg.startswith("#") and bg.startswith("#"):
                    label = (path.name, tinycss2.serialize(rule.prelude).strip())
                    self.assertGreaterEqual(contrast(fg, bg), 4.5, label)
                    if path == GTK / "common.css":
                        self.assertEqual(values["background-image"], "none", label)

    def test_semantic_and_disabled_checked_button_contract(self):
        selectors = {}
        for rule in stylesheet(GTK / "common.css"):
            if rule.type == "qualified-rule":
                for selector in tinycss2.serialize(rule.prelude).split(","):
                    selectors.setdefault(selector.strip(), {}).update(css_values(rule))
        for name, bg in (("suggested-action", "#174ea6"), ("destructive-action", "#a50e0e")):
            for state in ("", ":hover", ":active", ":checked", ":backdrop:checked"):
                values = selectors[f"button.{name}{state}"]
                self.assertEqual((values["color"], values["background-color"]), ("#ffffff", bg))
            for state in (":disabled", ":disabled:checked", ":disabled:backdrop:checked"):
                values = selectors[f"button.{name}{state}"]
                self.assertEqual((values["color"], values["background-color"]), ("#595d62", "#ffffff"))
        for selector in (
            "entry selection",
            "row:selected",
            "row.activatable:selected:hover",
            "textview text selection",
        ):
            self.assertEqual(selectors[selector]["color"], "#202124")
            self.assertEqual(selectors[selector]["background-color"], "#d2e3fc")
        self.assertEqual(selectors["*"]["font-family"], '"Google Sans"')
        self.assertEqual(selectors[".monospace"]["font-family"], '"Google Sans Code"')

    def test_gtk3_public_named_color_pairs(self):
        colors = {}
        for rule in stylesheet(GTK / "gtk-3.0/gtk.css"):
            if rule.type == "at-rule" and rule.lower_at_keyword == "define-color":
                name, value = tinycss2.serialize(rule.prelude).strip().split()
                colors[name] = value
        for prefix in ("theme_", "theme_unfocused_"):
            for fg, bg in (
                ("fg_color", "bg_color"),
                ("text_color", "base_color"),
                ("selected_fg_color", "selected_bg_color"),
            ):
                self.assertGreaterEqual(contrast(colors[prefix + fg], colors[prefix + bg]), 4.5)
        for fg in (
            "insensitive_fg_color",
            "unfocused_insensitive_color",
            "warning_color",
            "error_color",
            "success_color",
        ):
            self.assertGreaterEqual(contrast(colors[fg], "#ffffff"), 4.5)

    def test_gtk2_native_states_and_specialized_overrides(self):
        source = (GTK / "gtk-2.0/gtkrc").read_text()
        blocks = re.findall(r'style "([^"]+)"(?: = "[^"]+")? \{(.*?)\n\}', source, re.DOTALL)
        styles = {}
        for name, body in blocks:
            values = dict(styles.get("fmind-default", {}))
            values.update(
                {
                    (role, state): color
                    for role, state, color in re.findall(r'(fg|bg|text|base)\[(\w+)\] = "(#[0-9a-f]{6})"', body)
                }
            )
            styles[name] = values
            for state in ("NORMAL", "PRELIGHT", "ACTIVE", "SELECTED", "INSENSITIVE"):
                for fg, bg in (("fg", "bg"), ("text", "base")):
                    self.assertGreaterEqual(contrast(values[fg, state], values[bg, state]), 4.5, (name, state))
        self.assertEqual(styles["fmind-default"]["bg", "NORMAL"], "#ffffff")
        self.assertEqual(styles["fmind-menu-item"]["bg", "PRELIGHT"], "#d2e3fc")
        self.assertEqual(styles["fmind-progress"]["bg", "PRELIGHT"], "#174ea6")
        self.assertEqual(styles["fmind-progress"]["fg", "PRELIGHT"], "#ffffff")
        self.assertIn('engine "" {}', source)
        self.assertNotRegex(source, r'\binclude\b|engine "[^"\n]+"')

    def test_unity_companion_and_application_refinements(self):
        import xml.etree.ElementTree as ET

        unity = GTK / "unity"
        self.assertTrue(unity.is_dir())
        buttons = ("close", "minimize", "maximize", "unmaximize")
        states = (
            "focused_normal",
            "focused_prelight",
            "focused_pressed",
            "unfocused",
            "unfocused_prelight",
            "unfocused_pressed",
        )
        for btn in buttons:
            self.assertTrue((unity / f"{btn}.svg").is_symlink())
            self.assertEqual((unity / f"{btn}.svg").resolve(), (unity / f"{btn}_focused_normal.svg").resolve())
            for state in states:
                path = unity / f"{btn}_{state}.svg"
                self.assertTrue(path.is_file(), path)
                root = ET.fromstring(path.read_text())
                circle = root.find("{http://www.w3.org/2000/svg}circle")
                self.assertIsNotNone(circle)
                path_elem = root.find("{http://www.w3.org/2000/svg}path")
                self.assertIsNotNone(path_elem)
                bg = circle.attrib["fill"]
                fg = path_elem.attrib["stroke"]
                self.assertGreaterEqual(contrast(fg, bg), 4.5, (btn, state, fg, bg))

        common = (GTK / "common.css").read_text()
        for selector in (
            "GtkButton",
            "GtkEntry",
            "GtkTextView",
            "GtkTreeView",
            "GtkHeaderBar",
            "GtkNotebook",
            "GtkSwitch",
            ".nemo-window",
            "ThunarWindow",
            "CajaNavigationWindow",
            ".geary-main-window",
            "UnityDecoration",
            "UnityPanelWidget",
            ".xfce4-panel",
            ".mate-panel-menu-bar",
            ".budgie-panel",
            "#lightdm-user-pass",
        ):
            self.assertIn(selector, common, f"Missing selector {selector} in common.css")


if __name__ == "__main__":
    unittest.main()
