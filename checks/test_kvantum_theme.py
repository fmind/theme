"""Kvantum palette, native SVG closure and widget-state coverage."""

import unittest
import xml.etree.ElementTree as ET

from test_kde_theme import HREF, NS, config
from test_theme import ROOT, contrast

THEME = ROOT / "gtk/kde/kvantum/Fmind"
STATES = {"normal", "focused", "pressed", "toggled", "disabled"}
PARTS = {"top", "bottom", "left", "right", "topleft", "topright", "bottomleft", "bottomright"}
SECTIONS = {
    "PanelButtonCommand",
    "PanelButtonTool",
    "Dock",
    "DockTitle",
    "IndicatorSpinBox",
    "RadioButton",
    "CheckBox",
    "Focus",
    "GenericFrame",
    "LineEdit",
    "DropDownButton",
    "IndicatorArrow",
    "ToolboxTab",
    "Tab",
    "TabFrame",
    "TabBarFrame",
    "TreeExpander",
    "HeaderSection",
    "SizeGrip",
    "Toolbar",
    "ToolbarButton",
    "ToolbarComboBox",
    "ToolbarLineEdit",
    "Slider",
    "SliderCursor",
    "Progressbar",
    "ProgressbarContents",
    "ItemView",
    "Splitter",
    "Scrollbar",
    "ScrollbarGroove",
    "ScrollbarSlider",
    "Menu",
    "MenuItem",
    "MenuBar",
    "MenuBarItem",
    "TitleBar",
    "ComboBox",
    "GroupBox",
    "ToolTip",
    "StatusBar",
    "Window",
    "Dialog",
}


def resolved(settings, section):
    """Follow the same explicit per-section inheritance used by Kvantum."""
    chain = set()
    result = {}
    while section:
        if section in chain:
            raise ValueError(f"Cyclic Kvantum inheritance at {section}")
        chain.add(section)
        result = dict(settings[section]) | result
        section = settings[section].get("inherits")
    return result


def svg():
    root = ET.parse(THEME / "Fmind.svg").getroot()
    nodes = [n for n in root.iter() if "id" in n.attrib]
    ids = {n.attrib["id"]: n for n in nodes}
    if len(ids) != len(nodes):
        raise ValueError("Duplicate Kvantum SVG IDs")
    return root, ids


class KvantumThemeTests(unittest.TestCase):
    def test_palette_keeps_ordinary_and_mdi_surfaces_white(self):
        settings = config(THEME / "Fmind.kvconfig")
        colors = settings["GeneralColors"]
        for role in (
            "window",
            "inactive.window",
            "base",
            "inactive.base",
            "alt.base",
            "inactive.alt.base",
            "button",
            "tooltip.base",
            "dark",
        ):
            # Qt uses Dark as the default QMdiArea workspace background.
            self.assertEqual(colors[f"{role}.color"], "#ffffff", role)
        for fg, bg in (
            ("text", "base"),
            ("window.text", "window"),
            ("button.text", "button"),
            ("tooltip.text", "tooltip.base"),
            ("highlight.text", "highlight"),
            ("inactive.highlight.text", "inactive.highlight"),
        ):
            self.assertGreaterEqual(contrast(colors[f"{fg}.color"], colors[f"{bg}.color"]), 4.5)
        for bg in ("#ffffff", "#d2e3fc", "#ceead6", "#f1f3f4"):
            self.assertGreaterEqual(contrast(colors["disabled.text.color"], bg), 4.5)
        self.assertEqual(
            (THEME / "Fmind.colors").read_bytes(), (ROOT / "gtk/kde/color-schemes/Fmind.colors").read_bytes()
        )

    def test_widget_sections_resolve_to_native_assets(self):
        settings = config(THEME / "Fmind.kvconfig")
        self.assertEqual(set(settings.sections()), SECTIONS | {"%General", "GeneralColors", "Hacks"})
        _, ids = svg()
        for section in SECTIONS:
            values = resolved(settings, section)
            if values.get("frame") == "true":
                prefix = values["frame.element"]
                for part in PARTS:
                    if section == "Focus":
                        self.assertIn(f"{prefix}-{part}", ids)
                    else:
                        for state in STATES:
                            self.assertIn(f"{prefix}-{state}-{part}", ids, section)
            if values.get("interior") == "true":
                prefix = values["interior.element"]
                states = {"normal", "focused"} if section in {"CheckBox", "RadioButton"} else STATES
                for state in states:
                    self.assertIn(f"{prefix}-{state}", ids, section)
            for state in ("normal", "focus", "press", "toggle"):
                self.assertGreaterEqual(contrast(values[f"text.{state}.color"], "#d2e3fc"), 4.5)

    def test_svg_references_and_indicator_coverage(self):
        root, ids = svg()
        for node in root.iter():
            self.assertIn(node.tag.split("}")[-1], {"svg", "g", "rect", "circle", "path", "use"})
            self.assertNotIn("opacity", node.attrib)
            if HREF in node.attrib:
                target = node.attrib[HREF]
                self.assertTrue(target.startswith("#"))
                self.assertIn(target[1:], ids)
                self.assertNotIn(HREF, ids[target[1:]].attrib)
        for prefix in (
            "arrow-up",
            "arrow-down",
            "arrow-left",
            "arrow-right",
            "arrow-plus",
            "arrow-minus",
            "tab-close",
            "mdi-close",
            "mdi-maximize",
            "mdi-restore",
            "mdi-minimize",
            "mdi-shade",
            "mdi-menu",
            "sizegrip",
        ):
            for state in STATES:
                self.assertIn(f"{prefix}-{state}", ids)
        for kind in ("checkbox", "radio"):
            for state in ("normal", "focused"):
                self.assertIn(f"{kind}-checked-{state}", ids)
                if kind == "checkbox":
                    self.assertIn(f"{kind}-tristate-{state}", ids)
        for name in (
            "dial",
            "dial-notches",
            "dial-handle",
            "toolbar-separator",
            "toolbar-handle",
            "menuitem-separator",
            "header-separator",
            "button-default-indicator",
        ):
            self.assertIn(name, ids)

    def test_disabled_progress_retains_a_visible_fill(self):
        _, ids = svg()
        disabled = ids["progress-disabled"]
        if HREF in disabled.attrib:
            disabled = ids[disabled.get(HREF)[1:]]
        fill = disabled.find("s:rect", NS).get("fill")
        self.assertEqual(fill, "#ceead6")
        settings = config(THEME / "Fmind.kvconfig")
        self.assertGreaterEqual(contrast(settings["GeneralColors"]["progress.indicator.text.color"], fill), 4.5)

    def test_opaque_effect_policy(self):
        settings = config(THEME / "Fmind.kvconfig")
        general = settings["%General"]
        for key in ("composite", "translucent_windows", "blurring", "popup_blurring", "respect_DE"):
            self.assertFalse(general.getboolean(key))
        for key in ("menu_shadow_depth", "tooltip_shadow_depth", "reduce_window_opacity", "reduce_menu_opacity"):
            self.assertEqual(general.getint(key), 0)
        self.assertGreaterEqual(general.getint("progressbar_thickness"), 24)
        self.assertEqual(settings["Hacks"].getint("disabled_icon_opacity"), 100)


if __name__ == "__main__":
    unittest.main()
