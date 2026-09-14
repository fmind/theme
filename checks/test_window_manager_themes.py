"""Native window decoration coverage, asset geometry and state contrast."""

import ast
import configparser
import re
import unittest
import xml.etree.ElementTree as ET

from test_theme import ROOT, contrast

GTK = ROOT / "gtk"
VARIANTS = {
    1: GTK / "xfwm4",
    2: GTK / "variants/Fmind-hdpi/xfwm4",
    3: GTK / "variants/Fmind-xhdpi/xfwm4",
}
BUTTONS = {"menu", "stick", "shade", "hide", "maximize", "close"}
TOGGLES = {"stick", "shade", "maximize"}
FRAME_PARTS = {
    *(f"title-{i}" for i in range(1, 6)),
    "top-left",
    "top-right",
    "left",
    "right",
    "bottom",
    "bottom-left",
    "bottom-right",
}


def xpm(path):
    """Decode the explicit one-character native XPM subset used by this theme."""
    strings = re.findall(r'^"([^"\n]*)",?$', path.read_text(), re.MULTILINE)
    width, height, count, chars = map(int, strings[0].split())
    if chars != 1 or len(strings) != 1 + count + height:
        raise ValueError(f"Invalid XPM dimensions: {path.name}")
    colors = {}
    for entry in strings[1 : count + 1]:
        symbol, value = entry.split(" c ")
        if len(symbol) != 1 or symbol in colors:
            raise ValueError(f"Invalid XPM symbol: {path.name}")
        colors[symbol] = value
    rows = strings[count + 1 :]
    if any(len(row) != width or not set(row) <= colors.keys() for row in rows):
        raise ValueError(f"Invalid XPM pixels: {path.name}")
    return width, height, colors, rows


class WindowManagerThemeTests(unittest.TestCase):
    def test_xfwm_complete_native_parts_and_button_states(self):
        expected = {f"{part}-{state}.xpm" for part in FRAME_PARTS for state in ("active", "inactive")}
        for button in BUTTONS:
            for state in ("active", "inactive", "prelight", "pressed"):
                expected.add(f"{button}-{state}.xpm")
                if button in TOGGLES:
                    expected.add(f"{button}-toggled-{state}.xpm")
        for directory in VARIANTS.values():
            self.assertEqual({p.name for p in directory.glob("*.xpm")}, expected)
            for name in expected:
                _, _, colors, rows = xpm(directory / name)
                if name.split("-")[0] not in BUTTONS:
                    self.assertIn("#ffffff", colors.values())
                if "X" in colors:
                    self.assertTrue(any("X" in row for row in rows), name)
                    self.assertGreaterEqual(contrast(colors["X"], colors["."]), 4.5, name)

    def test_xfwm_high_dpi_geometry_and_pixels(self):
        for original in VARIANTS[1].glob("*.xpm"):
            width, height, colors, rows = xpm(original)
            for scale in (2, 3):
                sw, sh, sc, sr = xpm(VARIANTS[scale] / original.name)
                self.assertEqual((sw, sh, sc), (width * scale, height * scale, colors), original.name)
                self.assertEqual(
                    sr, ["".join(c * scale for c in row) for row in rows for _ in range(scale)], original.name
                )

    def test_xfwm_settings_and_toggled_glyphs(self):
        for scale, directory in VARIANTS.items():
            config = configparser.ConfigParser()
            config.read_string("[theme]\n" + (directory / "themerc").read_text())
            theme = config["theme"]
            for focus in ("active", "inactive"):
                bg = theme[f"{focus}_color_1"]
                self.assertEqual(bg, "#ffffff")
                self.assertGreaterEqual(contrast(theme[f"{focus}_text_color"], bg), 4.5)
                self.assertFalse(theme.getboolean(f"title_shadow_{focus}"))
            self.assertEqual(theme.getint("button_spacing"), 2 * scale)
            self.assertEqual(theme.getint("frame_border_top"), scale)
            self.assertEqual(theme["title_font"], "Google Sans Bold 10")
            self.assertNotIn("button_layout", theme)
            for button in TOGGLES:
                normal = xpm(directory / f"{button}-active.xpm")
                toggled = xpm(directory / f"{button}-toggled-active.xpm")
                self.assertNotEqual(normal[3], toggled[3], button)
                self.assertEqual(toggled[2]["."], "#d2e3fc")

    def test_metacity_frame_states_and_reference_closure(self):
        root = ET.parse(GTK / "metacity-1/metacity-theme-3.xml").getroot()
        groups = {
            tag: {node.attrib["name"]: node for node in root.findall(tag)}
            for tag in ("frame_geometry", "frame_style", "frame_style_set", "draw_ops")
        }
        for tag, nodes in groups.items():
            self.assertEqual(len(nodes), len(root.findall(tag)), tag)
            for node in nodes.values():
                if "parent" in node.attrib:
                    self.assertIn(node.attrib["parent"], nodes)
        for node in root.iter():
            for attribute, group in (
                ("geometry", "frame_geometry"),
                ("style", "frame_style"),
                ("style_set", "frame_style_set"),
                ("draw_ops", "draw_ops"),
            ):
                if attribute in node.attrib:
                    self.assertIn(node.attrib[attribute], groups[group])
            if node.tag == "include":
                self.assertIn(node.attrib["name"], groups["draw_ops"])
        self.assertEqual(
            {n.attrib["type"] for n in root.findall("window")},
            {"normal", "dialog", "modal_dialog", "utility", "menu", "border"},
        )
        states = {
            "normal",
            "shaded",
            "maximized",
            "tiled_left",
            "tiled_right",
            "maximized_and_shaded",
            "tiled_left_and_shaded",
            "tiled_right_and_shaded",
        }
        for style_set in groups["frame_style_set"].values():
            actual = {(n.attrib["focus"], n.attrib["state"], n.get("resize")) for n in style_set}
            expected = {
                (focus, state, resize)
                for focus in ("yes", "no")
                for state in states
                for resize in (("none", "vertical", "horizontal", "both") if state in {"normal", "shaded"} else (None,))
            }
            self.assertEqual(actual, expected)

    def test_metacity_all_controls_and_painted_contrast(self):
        root = ET.parse(GTK / "metacity-1/metacity-theme-3.xml").getroot()
        ops = {n.attrib["name"]: n for n in root.findall("draw_ops")}
        controls = {"close", "minimize", "maximize", "menu", "shade", "unshade", "above", "unabove", "stick", "unstick"}
        buttons = root.find("frame_style[@name='normal_active']").findall("button")
        self.assertEqual(
            {(b.attrib["function"], b.attrib["state"]) for b in buttons},
            {(a, s) for a in controls for s in ("normal", "prelight", "pressed")},
        )
        for button in buttons:
            draw = ops[button.attrib["draw_ops"]]
            background = draw.find("rectangle").attrib["color"]
            glyph = ops[draw.find("include").attrib["name"]]
            self.assertTrue(len(glyph), button.attrib)
            for line in glyph:
                self.assertGreaterEqual(contrast(line.attrib["color"], background), 4.5)
        for name in ("title_active", "title_inactive"):
            self.assertGreaterEqual(contrast(ops[name].find("title").attrib["color"], "#ffffff"), 4.5)
        for name in ("maximized_active", "maximized_inactive"):
            buttons = root.find(f"frame_style[@name='{name}']").findall("button")
            self.assertEqual(
                {b.attrib["draw_ops"] for b in buttons}, {f"restore_{s}" for s in ("normal", "prelight", "pressed")}
            )

    def test_metacity_coordinates_avoid_unsupported_unary_operators(self):
        root = ET.parse(GTK / "metacity-1/metacity-theme-3.xml").getroot()
        # Metacity accepts these strings while parsing, but rejects unary minus
        # during painting. Keep our arithmetic inside its supported binary subset.
        allowed = (ast.Expression, ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Name, ast.Load, ast.Constant)
        for ops in root.findall("draw_ops"):
            for node in ops:
                for key in ("x", "y", "x1", "y1", "x2", "y2", "width", "height"):
                    if key in node.attrib:
                        expression = ast.parse(node.attrib[key], mode="eval")
                        self.assertTrue(all(isinstance(n, allowed) for n in ast.walk(expression)), node.attrib)
        self.assertEqual(root.findall(".//image"), [])


if __name__ == "__main__":
    unittest.main()
