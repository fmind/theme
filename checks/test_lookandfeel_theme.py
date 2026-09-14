"""KDE global-theme references, fonts and native package preview integrity."""

import json
import struct
import unittest

from test_kde_theme import config
from test_theme import ROOT

KDE = ROOT / "gtk/kde"
THEME = KDE / "plasma/look-and-feel/Fmind"


class LookAndFeelTests(unittest.TestCase):
    def test_plasma_metadata_agrees_across_versions(self):
        modern = json.loads((THEME / "metadata.json").read_text())
        legacy = config(THEME / "metadata.desktop")["Desktop Entry"]
        self.assertEqual(modern["KPackageStructure"], "Plasma/LookAndFeel")
        self.assertEqual(modern["KPlugin"]["ServiceTypes"], [legacy["X-KDE-ServiceTypes"]])
        self.assertEqual(modern["KPlugin"]["Id"], THEME.name)
        self.assertEqual(legacy["X-KDE-PluginInfo-Name"], THEME.name)
        self.assertEqual(modern["KPlugin"]["Version"], legacy["X-KDE-PluginInfo-Version"])

    def test_defaults_reference_shipped_components(self):
        defaults = config(THEME / "contents/defaults")
        general = defaults["kdeglobals][General"]
        self.assertTrue((KDE / "color-schemes" / (general["ColorScheme"] + ".colors")).is_file())
        style = defaults["plasmarc][Theme"]["name"]
        self.assertTrue((KDE / "plasma/desktoptheme" / style / "metadata.json").is_file())
        decoration = defaults["kwinrc][org.kde.kdecoration2"]
        self.assertEqual(decoration["library"], "org.kde.kwin.aurorae")
        self.assertTrue((KDE / "aurorae" / decoration["theme"].removeprefix("__aurorae__svg__") / "Fmindrc").is_file())
        self.assertEqual(defaults["kdeglobals][KDE"]["widgetStyle"], "kvantum")
        self.assertTrue((KDE / "kvantum/Fmind/Fmind.kvconfig").is_file())
        self.assertEqual(defaults["ksplashrc][KSplash"]["Theme"], THEME.name)
        self.assertEqual(defaults["ksplashrc][KSplash"]["Engine"], "KSplashQML")
        self.assertTrue((THEME / "contents/splash/Splash.qml").is_file())
        cursor = defaults["kcminputrc][Mouse"]["cursorTheme"]
        self.assertTrue((KDE / "cursors" / cursor / "cursors/default").is_file())
        self.assertEqual((THEME / "contents/colors").read_bytes(), (KDE / "color-schemes/Fmind.colors").read_bytes())

    def test_font_defaults_cover_ui_monospace_and_titles(self):
        defaults = config(THEME / "contents/defaults")
        general = defaults["kdeglobals][General"]
        for key in ("font", "smallestReadableFont", "toolBarFont", "menuFont"):
            self.assertEqual(general[key].split(",")[0], "Google Sans")
        self.assertEqual(general["fixed"].split(",")[0], "Google Sans Code")
        self.assertEqual(defaults["kdeglobals][WM"]["activeFont"].split(",")[0], "Google Sans")

    def test_package_previews_are_valid_internal_pngs(self):
        for name in ("preview.png", "splash.png"):
            path = THEME / "contents/previews" / name
            self.assertTrue(path.resolve().is_relative_to(THEME.resolve()))
            data = path.read_bytes()
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(data[12:16], b"IHDR")
            self.assertEqual(struct.unpack(">II", data[16:24]), (960, 540))
            self.assertIn(b"IEND", data[-12:])


if __name__ == "__main__":
    unittest.main()
