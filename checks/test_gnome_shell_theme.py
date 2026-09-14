"""GNOME Shell cascade regressions, native control variants and capture masks."""

import re
import unittest
import xml.etree.ElementTree as ET

import tinycss2
from test_gtk_ports import css_values, stylesheet
from test_theme import ROOT, contrast

SHELL = ROOT / "gtk/gnome-shell"


def specificity(selector):
    """The shipped St subset has IDs, classes, pseudo-classes and widget names."""
    return (
        selector.count("#"),
        selector.count(".") + selector.count(":"),
        len(re.findall(r"(?:^|[\s>])([A-Za-z_][\w-]*)", selector)),
    )


def values(path):
    result = {}
    for rule in stylesheet(path):
        if rule.type == "qualified-rule":
            for selector in tinycss2.serialize(rule.prelude).split(","):
                result.setdefault(selector.strip(), {}).update(css_values(rule))
    return result


class GnomeShellThemeTests(unittest.TestCase):
    def test_entry_points_and_local_resource_closure(self):
        for name in ("gnome-shell.css", "legacy.css"):
            imports = [r for r in stylesheet(SHELL / name) if r.type == "at-rule"]
            self.assertEqual(len(imports), 1)
            self.assertEqual(imports[0].lower_at_keyword, "import")
            self.assertEqual(tinycss2.serialize(imports[0].prelude).strip(), 'url("common.css")')
        referenced = set()
        for path in SHELL.glob("*.css"):
            for target in re.findall(r'url\("([^"\n]+)"\)', path.read_text()):
                self.assertFalse(":" in target or target.startswith("/"), (path.name, target))
                resolved = (path.parent / target).resolve()
                self.assertTrue(resolved.is_relative_to(ROOT / "gtk"))
                self.assertTrue(resolved.is_file(), target)
                if resolved.suffix == ".svg":
                    referenced.add(resolved)
                    root = ET.parse(resolved).getroot()
                    width, height = int(root.attrib["width"]), int(root.attrib["height"])
                    self.assertEqual(root.attrib["viewBox"], f"0 0 {width} {height}")
                    self.assertTrue(all("href" not in key for n in root.iter() for key in n.attrib))
        self.assertEqual(len(referenced), 11)
        self.assertLessEqual(set((SHELL / "assets").glob("*.svg")), referenced)

    def test_imported_colors_survive_native_cascade_order(self):
        for rule in stylesheet(SHELL / "common.css"):
            if rule.type != "qualified-rule":
                continue
            selectors = [s.strip() for s in tinycss2.serialize(rule.prelude).split(",")]
            # St stores the last matching selector's specificity for the entire rule.
            priorities = [specificity(s) for s in selectors]
            self.assertEqual(priorities, sorted(priorities), selectors)
            for declaration in tinycss2.parse_declaration_list(rule.content, skip_comments=True, skip_whitespace=True):
                # Imported sheets lose application origin: native labels and hover
                # colors otherwise beat equally specific imported declarations.
                self.assertTrue(declaration.important, (selectors, declaration.name))

    def test_modern_native_controls_and_legacy_image_states(self):
        modern = values(SHELL / "gnome-shell.css")
        legacy = values(SHELL / "legacy.css")
        self.assertEqual(modern[".check-box StIcon"]["color"], "transparent")
        for state in (":checked", ":checked:hover", ":checked:active"):
            checked = modern[f".check-box{state} StIcon"]
            self.assertGreaterEqual(contrast(checked["color"], checked["background-color"]), 4.5)
        for state, background in (("", "#595d62"), (":checked", "#174ea6")):
            self.assertEqual(modern[f".toggle-switch{state} .handle"]["background-color"], background)
        self.assertNotIn("opacity", modern[".toggle-switch .handle"])
        for control, off, on in (
            ("check", ".check-box StBin", ".check-box:checked StBin"),
            ("switch", ".toggle-switch", ".toggle-switch:checked"),
        ):
            before, after = legacy[off]["background-image"], legacy[on]["background-image"]
            self.assertIn("-off.svg", before, control)
            self.assertIn("-on.svg", after, control)
            self.assertNotEqual(before, after)
        self.assertEqual(
            legacy[".check-box:checked:focus StBin"]["background-image"],
            legacy[".check-box:checked StBin"]["background-image"],
        )

    def test_text_surfaces_feedback_and_capture_transparency(self):
        common = values(SHELL / "common.css")
        for selector in (
            "#panel",
            "#panel:overview",
            ".popup-menu-content",
            ".quick-settings",
            ".modal-dialog",
            ".osd-window",
            ".screenshot-ui-panel",
            ".app-label",
            ".window-caption",
            ".unlock-dialog-clock",
        ):
            self.assertEqual(common[selector]["background-color"], "#ffffff", selector)
            self.assertGreaterEqual(contrast(common[selector]["color"], "#ffffff"), 4.5, selector)
        for selector in (".lightbox", ".screenshot-ui-area-indicator-shade"):
            self.assertEqual(common[selector]["background-color"], "rgba(32, 33, 36, 0.32)")
        self.assertEqual(
            common[".screenshot-ui-area-selector .screenshot-ui-area-indicator-selection"]["background-color"],
            "transparent",
        )
        self.assertEqual(
            common[".screenshot-ui-capture-button:cast .screenshot-ui-capture-button-circle"]["background-color"],
            "#a50e0e",
        )
        for selector in (".hidden", "#appMenu .label-shadow", ".screenshot-ui-window-selector-check"):
            self.assertEqual(common[selector]["color"], "transparent")
        self.assertEqual(common[".window-close"]["background-image"], "none")
        self.assertEqual(common[".slider"]["-barlevel-overdrive-color"], "#a50e0e")
        self.assertEqual(common[".lg-dialog .shell-link"]["color"], "#174ea6")
        self.assertEqual(common["stage"]["font-family"], '"Google Sans"')
        self.assertEqual(common["#LookingGlassDialog"]["font-family"], '"Google Sans Code"')


if __name__ == "__main__":
    unittest.main()
