"""Aurorae package closure, accessible states and native layout constraints."""

import unittest
import xml.etree.ElementTree as ET

from test_kde_theme import HREF, NS, color, config
from test_theme import ROOT, contrast

THEME = ROOT / "gtk/kde/aurorae/Fmind"
BUTTONS = {
    "close",
    "minimize",
    "maximize",
    "restore",
    "alldesktops",
    "keepabove",
    "keepbelow",
    "shade",
    "help",
    "appmenu",
    "menu",
}
STATES = {
    "active",
    "inactive",
    "hover",
    "hover-inactive",
    "pressed",
    "pressed-inactive",
    "deactivated",
    "deactivated-inactive",
}
PARTS = {"center", "top", "bottom", "left", "right", "topleft", "topright", "bottomleft", "bottomright"}


def elements(path):
    root = ET.parse(path).getroot()
    nodes = [n for n in root.iter() if "id" in n.attrib]
    ids = {n.attrib["id"]: n for n in nodes}
    if len(ids) != len(nodes):
        raise ValueError(f"Duplicate SVG IDs in {path.name}")
    for node in root.iter():
        if HREF in node.attrib and (not node.attrib[HREF].startswith("#") or node.attrib[HREF][1:] not in ids):
            raise ValueError(f"Unresolved SVG reference in {path.name}")
    return root, ids


class AuroraeThemeTests(unittest.TestCase):
    def test_package_identity_and_native_asset_completeness(self):
        metadata = config(THEME / "metadata.desktop")["Desktop Entry"]
        self.assertEqual(metadata["Name"], THEME.name)
        self.assertEqual(metadata["X-KDE-PluginInfo-Name"], THEME.name)
        self.assertTrue((THEME / f"{THEME.name}rc").is_file())
        self.assertEqual({p.stem for p in THEME.glob("*.svg")}, BUTTONS | {"decoration"})
        for path in THEME.glob("*.svg"):
            root, _ = elements(path)
            for node in root.iter():
                self.assertIn(node.tag.split("}")[-1], {"svg", "g", "rect", "path", "use"})
                self.assertNotIn("opacity", node.attrib)
                self.assertNotIn("style", node.attrib)

    def test_button_states_keep_glyphs_readable_and_toggles_visible(self):
        for name in BUTTONS:
            _, ids = elements(THEME / f"{name}.svg")
            self.assertEqual(set(ids), {f"{state}-center" for state in STATES})
            for state in STATES:
                node = ids[f"{state}-center"]
                background = node.find("s:rect", NS)
                glyph = node.find("s:path", NS)
                self.assertEqual((background.get("width"), background.get("height")), ("28", "28"))
                self.assertTrue(glyph.get("d"), (name, state))
                self.assertGreaterEqual(contrast(glyph.get("stroke"), background.get("fill")), 4.5, (name, state))
                if state in {"active", "inactive", "deactivated", "deactivated-inactive"}:
                    self.assertEqual(background.get("fill"), "#ffffff")
            if name in {"alldesktops", "keepabove", "keepbelow", "shade"}:
                for suffix in ("", "-inactive"):
                    normal = ids[("inactive" if suffix else "active") + "-center"]
                    pressed = ids[f"pressed{suffix}-center"]
                    self.assertNotEqual(normal.find("s:rect", NS).get("fill"), pressed.find("s:rect", NS).get("fill"))
        _, shade = elements(THEME / "shade.svg")
        self.assertNotEqual(
            shade["active-center"].find("s:path", NS).get("d"), shade["pressed-center"].find("s:path", NS).get("d")
        )

    def test_frame_states_and_ordinary_white_surfaces(self):
        _, ids = elements(THEME / "decoration.svg")
        for state in ("decoration", "decoration-inactive", "decoration-opaque", "decoration-opaque-inactive"):
            for part in PARTS:
                node = ids[f"{state}-{part}"]
                if HREF in node.attrib:
                    node = ids[node.get(HREF)[1:]]
                self.assertEqual(node.find("s:rect", NS).get("fill"), "#ffffff")
        for suffix in ("", "-inactive", "-opaque", "-opaque-inactive"):
            self.assertIn(f"decoration-maximized{suffix}-center", ids)
        self.assertFalse(any(key.startswith("mask") for key in ids))

    def test_title_contrast_and_edge_reachable_maximized_controls(self):
        theme = config(THEME / "Fmindrc")
        general, layout = theme["General"], theme["Layout"]
        for state in ("Active", "Inactive"):
            self.assertGreaterEqual(contrast(color(general[f"{state}TextColor"]), "#ffffff"), 4.5)
        for option in ("UseTextShadow", "HaloActive", "HaloInactive", "Shadow"):
            self.assertFalse(general.getboolean(option))
        self.assertEqual(general.getint("DecorationPosition"), 0)
        self.assertGreaterEqual(
            layout.getint("TitleHeight"), layout.getint("ButtonHeight") + layout.getint("ButtonMarginTop")
        )
        for side in ("Top", "Bottom", "Left", "Right"):
            self.assertEqual(layout.getint(f"TitleEdge{side}Maximized"), int(side == "Bottom"))
            self.assertEqual(layout.getint(f"Padding{side}"), 0)
        self.assertEqual(layout.getint("ButtonMarginTopMaximized"), 0)
        self.assertGreaterEqual(layout.getint("ButtonWidth"), 24)
        self.assertGreaterEqual(layout.getint("ButtonHeight"), 24)


if __name__ == "__main__":
    unittest.main()
