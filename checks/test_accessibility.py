"""Readability of essential controls, including non-text state indicators."""

import re
import unittest

import tinycss2
from test_gtk_ports import GTK, css_values, stylesheet
from test_theme import ROOT, contrast


class AccessibilityTests(unittest.TestCase):
    def test_fzf_scrollbar_position_is_visible(self):
        source = (ROOT / "fzf/fmind.conf").read_text()
        foreground = re.search(r"--color=scrollbar:(#[0-9a-f]{6})", source)[1]
        self.assertGreaterEqual(contrast(foreground, "#ffffff"), 3)

    def test_essential_gtk_controls(self):
        selectors = {}
        for rule in stylesheet(GTK / "common.css"):
            if rule.type == "qualified-rule":
                for selector in tinycss2.serialize(rule.prelude).split(","):
                    selectors.setdefault(selector.strip(), {}).update(css_values(rule))
        # These boundaries identify controls on otherwise identical white surfaces.
        for selector in ("button", "entry", "spinbutton", "combobox button", "check", "radio", "switch"):
            for surface in ("#ffffff", "#f1f3f4"):
                with self.subTest(selector=selector, surface=surface):
                    self.assertGreaterEqual(contrast(selectors[selector]["border-color"], surface), 3)
        for selector in ("scale slider", "scrollbar slider"):
            self.assertGreaterEqual(contrast(selectors[selector]["background-color"], "#ffffff"), 3, selector)
        for selector in ("button:focus", "entry:focus", "spinbutton:focus", "combobox button:focus"):
            self.assertGreaterEqual(contrast(selectors[selector]["outline-color"], "#ffffff"), 3, selector)
            self.assertNotEqual(selectors[selector]["outline-style"], "none")
        for selector in ("check:checked", "radio:checked", "switch:checked"):
            values = selectors[selector]
            self.assertGreaterEqual(contrast(values["color"], values["background-color"]), 3, selector)
        for name in ("suggested-action", "destructive-action"):
            outline = selectors[f"button.{name}:focus:not(:disabled)"]["outline-color"]
            self.assertGreaterEqual(contrast(outline, selectors[f"button.{name}"]["background-color"]), 3, name)
