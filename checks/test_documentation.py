"""Check catalog accounting and the published documentation's navigation."""

import re
import unittest
from html.parser import HTMLParser

import build_site as builder
from test_theme import APPS, ROOT


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "img":
            self.images.append(attrs["src"])


class DocumentationTests(unittest.TestCase):
    def test_catalog_snapshot_has_a_directory_for_each_entry(self):
        slugs = re.findall(r"https://draculatheme.com/([^\s)]+)", (ROOT / "TODO.md").read_text())
        self.assertEqual(len(slugs), 472)
        self.assertEqual(len(set(slugs)), len(slugs), "Duplicate reference catalog entry")
        aliases = {
            "NewTerm2": "newterm2",
            "WOB": "wob",
            "base16-dracula-scheme": "base16",
            "dRacula": "r",
            "google-chrome": "chrome",
            "iterm": "iterm2",
            "rio-terminal": "rio",
            "spyder-ide": "spyder",
            "sublime": "sublime-text",
            "visual-studio-code": "vscode",
        }
        directories = {app.name for app in APPS}
        for slug in slugs:
            self.assertIn(aliases.get(slug, slug), directories, slug)

    def test_readme_site_links_and_assets(self):
        page = builder.render((ROOT / "README.md").read_text())
        parser = Links()
        parser.feed(page)
        self.assertIn("<table>", page)
        self.assertIn("<pre><code", page)
        self.assertIn("<main>", page)
        self.assertIn("https://github.com/fmind/theme/blob/main/ghostty/fmind", parser.links)
        self.assertEqual(
            set(parser.images), {"screenshots/palette.svg", "screenshots/zellij.png", "screenshots/markdown.png"}
        )
        for src in parser.images:
            self.assertTrue((ROOT / src).is_file(), src)
        for link in parser.links:
            self.assertTrue(link.startswith(("https://", "#", "mailto:")), link)
