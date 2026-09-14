"""Cinnamon import boundary, control assets and readable feedback surfaces."""

import re
import unittest
import xml.etree.ElementTree as ET

import tinycss2
from test_gtk_ports import css_values, stylesheet
from test_theme import ROOT, contrast

CINNAMON = ROOT / "gtk/cinnamon"


def selectors():
    result = {}
    for rule in stylesheet(CINNAMON / "cinnamon.css"):
        if rule.type == "qualified-rule":
            for selector in tinycss2.serialize(rule.prelude).split(","):
                result.setdefault(selector.strip(), {}).update(css_values(rule))
    return result


class CinnamonThemeTests(unittest.TestCase):
    def test_native_import_and_complete_local_asset_closure(self):
        source = (CINNAMON / "cinnamon.css").read_text()
        rules = stylesheet(CINNAMON / "cinnamon.css")
        imports = [tinycss2.serialize(r.prelude).strip() for r in rules if r.type == "at-rule"]
        self.assertEqual(imports, ['url("/usr/share/cinnamon/theme/cinnamon.css")'])
        local = re.findall(r'url\("(assets/[^"\n]+)"\)', source)
        actual = {p.relative_to(CINNAMON).as_posix() for p in (CINNAMON / "assets").iterdir()}
        self.assertEqual(set(local), actual)
        self.assertEqual(len(actual), 13)
        for name in local:
            root = ET.parse(CINNAMON / name).getroot()
            self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
            width, height = int(root.attrib["width"]), int(root.attrib["height"])
            self.assertEqual(root.attrib["viewBox"], f"0 0 {width} {height}")
            self.assertGreater(width, 0)
            self.assertGreater(height, 0)
            # All controls are self-contained native vectors, with no linked resources or scripts.
            for node in root.iter():
                self.assertIn(node.tag.split("}")[-1], {"svg", "rect", "circle", "path", "line", "polyline"})
                self.assertFalse(any("href" in key for key in node.attrib), name)

    def test_checked_controls_have_distinct_visible_assets(self):
        values = selectors()
        for control, off, on in (
            (".toggle-switch", ".toggle-switch", ".toggle-switch:checked"),
            (".check-box", ".check-box StBin", ".check-box:checked StBin"),
            (".radiobutton", ".radiobutton StBin", ".radiobutton:checked StBin"),
        ):
            before = values[off]["background-image"]
            after = values[on]["background-image"]
            self.assertNotEqual(before, after, control)
            self.assertIn("-off.svg", before)
            self.assertIn("-on.svg", after)
        self.assertEqual(
            values[".popup-menu-item:active .toggle-switch:checked"]["background-image"],
            values[".toggle-switch:checked"]["background-image"],
        )
        self.assertEqual(
            values[".radiobutton:focus:checked StBin"]["background-image"],
            values[".radiobutton:checked StBin"]["background-image"],
        )

    def test_opaque_text_surfaces_and_meaningful_fill_contrast(self):
        values = selectors()
        for selector in ("#panel", ".popup-menu-content", ".dialog", "#notification", ".desklet", ".window-caption"):
            self.assertEqual(values[selector]["background-color"], "#ffffff", selector)
            self.assertGreaterEqual(contrast(values[selector]["color"], "#ffffff"), 4.5, selector)
        for selector in (".grouped-window-list-badge", ".media-keys-osd .level-bar", ".window-list-item-box .progress"):
            self.assertEqual(values[selector]["background-color"], "#174ea6", selector)
            self.assertGreaterEqual(contrast(values[selector]["color"], "#174ea6"), 4.5, selector)
        for property_name in ("warning-color", "error-color", "success-color"):
            self.assertGreaterEqual(contrast(values["stage"][property_name], "#ffffff"), 4.5)
        self.assertEqual(values[".media-keys-osd .level"]["-barlevel-amplify-color"], "#a50e0e")
        self.assertEqual(values["stage"]["font-family"], '"Google Sans"')
        self.assertEqual(values[".lg-dialog"]["font-family"], '"Google Sans Code"')


if __name__ == "__main__":
    unittest.main()
