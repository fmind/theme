"""KDE color roles, Plasma package integrity and readable native SVG states."""

import configparser
import json
import unittest
import xml.etree.ElementTree as ET

from test_theme import PALETTE, ROOT, contrast

KDE = ROOT / "gtk/kde"
STYLE = KDE / "plasma/desktoptheme/Fmind"
GROUPS = {f"Colors:{name}" for name in ("Button", "Complementary", "Header", "Selection", "Tooltip", "View", "Window")}
FOREGROUNDS = {
    f"Foreground{name}"
    for name in ("Normal", "Inactive", "Active", "Link", "Visited", "Negative", "Neutral", "Positive")
}
NS = {"s": "http://www.w3.org/2000/svg"}
HREF = "{http://www.w3.org/1999/xlink}href"


def config(path):
    result = configparser.ConfigParser()
    result.optionxform = str
    result.read(path)
    return result


def color(value):
    channels = tuple(map(int, value.split(",")))
    if len(channels) != 3 or any(c < 0 or c > 255 for c in channels):
        raise ValueError(f"Invalid native RGB value: {value}")
    return "#" + "".join(f"{c:02x}" for c in channels)


def center(root, prefix):
    nodes = {n.attrib["id"]: n for n in root.iter() if "id" in n.attrib}
    node = nodes[prefix + "-center"]
    while HREF in node.attrib:
        node = nodes[node.attrib[HREF][1:]]
    return node.find("s:rect", NS).attrib["fill"]


class KdeThemeTests(unittest.TestCase):
    def test_native_color_sets_and_selected_semantics(self):
        scheme = config(KDE / "color-schemes/Fmind.colors")
        allowed = set(PALETTE["official"] + PALETTE["custom"])
        for group in GROUPS | {"Colors:Header][Inactive"}:
            self.assertEqual(
                set(scheme[group]),
                FOREGROUNDS | {"BackgroundNormal", "BackgroundAlternate", "DecorationFocus", "DecorationHover"},
            )
            colors = {key: color(value) for key, value in scheme[group].items()}
            self.assertLessEqual(set(colors.values()), allowed)
            for fg in FOREGROUNDS:
                for bg in ("BackgroundNormal", "BackgroundAlternate"):
                    self.assertGreaterEqual(contrast(colors[fg], colors[bg]), 4.5, (group, fg, bg))
            expected = "#d2e3fc" if group == "Colors:Selection" else "#ffffff"
            self.assertEqual(colors["BackgroundNormal"], expected)
            self.assertEqual(colors["BackgroundAlternate"], expected)
        # KDE derives another fill from this role; amber failed native contrast
        # inside selections, while ordinary neutral feedback remains amber.
        self.assertEqual(color(scheme["Colors:Selection"]["ForegroundNeutral"]), "#202124")
        self.assertEqual(color(scheme["Colors:Window"]["ForegroundNeutral"]), "#934900")
        effects = scheme["ColorEffects:Disabled"]
        self.assertEqual(effects.getint("IntensityEffect"), 0)
        self.assertEqual(effects.getint("ColorEffect"), 0)
        self.assertLessEqual(effects.getfloat("ContrastAmount"), 0.08)
        self.assertFalse(scheme["ColorEffects:Inactive"].getboolean("ChangeSelectionColor"))

    def test_plasma_colors_match_application_scheme(self):
        scheme = config(KDE / "color-schemes/Fmind.colors")
        plasma = config(STYLE / "colors")
        self.assertNotIn("ColorEffects:Disabled", plasma)
        for group in GROUPS | {"Colors:Header][Inactive", "General", "KDE", "WM"}:
            self.assertEqual(dict(scheme[group]), dict(plasma[group]), group)
        for state in ("active", "inactive"):
            self.assertGreaterEqual(
                contrast(color(plasma["WM"][state + "Foreground"]), color(plasma["WM"][state + "Background"])), 4.5
            )

    def test_package_identity_and_opaque_effect_policy(self):
        metadata = json.loads((STYLE / "metadata.json").read_text())
        self.assertEqual(metadata["KPlugin"]["Id"], STYLE.name)
        self.assertEqual(metadata["KPlugin"]["Name"], "Fmind")
        self.assertEqual(metadata["X-Plasma-API"], "5.0")
        settings = config(STYLE / "plasmarc")
        self.assertEqual(settings["Settings"]["FallbackTheme"], "default")
        for effect in ("AdaptiveTransparency", "BlurBehindEffect", "ContrastEffect"):
            self.assertFalse(settings[effect].getboolean("enabled"))

    def test_svg_reference_closure_and_state_contrast(self):
        assets = list(STYLE.rglob("*.svg"))
        self.assertEqual(len(assets), 9)
        for path in assets:
            root = ET.parse(path).getroot()
            nodes = [n for n in root.iter() if "id" in n.attrib]
            ids = {n.attrib["id"] for n in nodes}
            self.assertEqual(len(ids), len(nodes), path.name)
            for node in root.iter():
                self.assertIn(node.tag.split("}")[-1], {"svg", "g", "rect", "use"})
                if HREF in node.attrib:
                    self.assertTrue(node.attrib[HREF].startswith("#"))
                    self.assertIn(node.attrib[HREF][1:], ids)
                self.assertNotIn("opacity", node.attrib)
            self.assertIn("center", ids)
            for side in ("top", "bottom", "left", "right"):
                self.assertIn(f"hint-{side}-margin", ids)
        for name, states in (
            ("viewitem", ("normal", "hover", "selected", "selected+hover")),
            ("tasks", ("normal", "hover", "focus", "attention", "minimized", "progress")),
        ):
            root = ET.parse(STYLE / "widgets" / f"{name}.svg").getroot()
            for state in states:
                for fg in ("#202124", "#595d62"):
                    self.assertGreaterEqual(contrast(fg, center(root, state)), 4.5, (name, state))
            if name == "tasks":
                for direction in ("north", "south", "east", "west"):
                    for state in states:
                        self.assertEqual(center(root, f"{direction}-{state}"), center(root, state))


if __name__ == "__main__":
    unittest.main()
