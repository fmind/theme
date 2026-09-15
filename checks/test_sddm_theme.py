"""SDDM package closure and the two supported virtual-keyboard style versions."""

import re
import struct
import unittest

from test_kde_theme import config
from test_theme import ROOT, contrast

THEME = ROOT / "gtk/kde/sddm/Fmind"


class SddmThemeTests(unittest.TestCase):
    def test_package_entry_points_and_preview(self):
        metadata = config(THEME / "metadata.desktop")["SddmGreeterTheme"]
        options = config(THEME / metadata["ConfigFile"])["General"]
        self.assertEqual(metadata["Theme-Id"], THEME.name)
        self.assertEqual(metadata["QtVersion"], options["qtVersion"])
        self.assertIn(options["batteryProvider"], {"plasma5", "plasma6"})
        self.assertEqual(options["showBattery"], "false")
        for key in ("MainScript", "ConfigFile", "Screenshot"):
            path = THEME / metadata[key]
            self.assertTrue(path.resolve().is_relative_to(THEME.resolve()))
            self.assertTrue(path.is_file(), path)
        png = (THEME / metadata["Screenshot"]).read_bytes()
        self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">II", png[16:24]), (960, 720))
        self.assertIn(b"IEND", png[-12:])

    def test_local_qml_components_resolve(self):
        for path in THEME.rglob("*.qml"):
            source = path.read_text()
            for name in re.findall(r'"([A-Z][\w]*\.qml)"', source):
                self.assertTrue((path.parent / name).is_file(), (path, name))
            for name in re.findall(r"\b(F[A-Z]\w*)\s*\{", source):
                self.assertTrue((path.parent / (name + ".qml")).is_file(), (path, name))

    def test_qt_major_styles_keep_the_same_appearance(self):
        styles = THEME / "QtQuick/VirtualKeyboard/Styles"
        for name in ("style.qml", "FKey.qml"):
            legacy = (styles / "Fmind" / name).read_text()
            modern = (styles / "Fmind6" / name).read_text()
            self.assertEqual(legacy.replace(" 2.4\n", "\n"), modern)
        legacy = (THEME / "VirtualKeyboard.qml").read_text()
        modern = (THEME / "VirtualKeyboard6.qml").read_text()
        self.assertEqual(legacy.replace(" 2.4\n", "\n").replace('"Fmind"', '"Fmind6"'), modern)

    def test_greeter_text_contrast_in_normal_selected_and_disabled_states(self):
        for foreground in ("#202124", "#595d62", "#174ea6", "#a50e0e"):
            for background in ("#ffffff", "#d2e3fc"):
                self.assertGreaterEqual(contrast(foreground, background), 4.5, (foreground, background))
            self.assertGreaterEqual(contrast("#934900", "#ffffff"), 4.5)

    def test_keyboard_dismissal_and_login_contracts(self):
        main = (THEME / "Main.qml").read_text()
        self.assertIn("ignoreUnknownSignals: true", main)
        self.assertIn("onLoaded: item.hidden.connect(function() { root.showKeyboard = false; })", main)
        self.assertIn("onShowKeyboardChanged: if (!showKeyboard) scroll.contentY = 0", main)
        self.assertIn("echoMode: TextInput.Password", main)
        self.assertIn("Qt.ImhHiddenText | Qt.ImhSensitiveData | Qt.ImhNoPredictiveText", main)
        self.assertIn("password.clear()", main)
        for name in ("VirtualKeyboard.qml", "VirtualKeyboard6.qml"):
            source = (THEME / name).read_text()
            self.assertIn("signal hidden()", source)
            self.assertIn("else if (root.activated) root.hidden();", source)


if __name__ == "__main__":
    unittest.main()
