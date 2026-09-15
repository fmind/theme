"""Check release metadata, the complete theme index and documentation navigation."""

import hashlib
import json
import re
import subprocess
import tomllib
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1] / "themes"
APPS = sorted(path for path in ROOT.iterdir() if path.is_dir() and not path.name.startswith((".", "__")))
PALETTE = yaml.safe_load((ROOT.parent / "checks/palette.yaml").read_text())


def contrast(a: str, b: str) -> float:
    def luminance(value):
        channels = [int(value[i : i + 2], 16) / 255 for i in (1, 3, 5)]
        linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
        return sum(c * weight for c, weight in zip(linear, (0.2126, 0.7152, 0.0722), strict=True))

    low, high = sorted((luminance(a), luminance(b)))
    return (high + 0.05) / (low + 0.05)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "img":
            self.images.append(attrs["src"])


class DocumentationTests(unittest.TestCase):
    def test_release_versions_are_consistent(self):
        version = tomllib.loads((ROOT.parent / "pyproject.toml").read_text())["project"]["version"]
        for path in ROOT.rglob("*.json"):
            if "node_modules" in path.parts or "labextension" in path.parts:
                continue
            doc = json.loads(path.read_text())
            if not isinstance(doc, dict):
                continue
            # Package versions only; leave native file-format/API versions intact.
            if path.name in ("package.json", "package-lock.json", "manifest.json", "extension.json", "ext.json"):
                if "version" in doc:
                    self.assertEqual(doc["version"], version, path)
                if path.name == "package-lock.json":
                    self.assertEqual(doc["packages"][""]["version"], version, path)
            if "KPlugin" in doc:
                self.assertEqual(doc["KPlugin"]["Version"], version, path)
        for path in ROOT.glob("*/pyproject.toml"):
            doc = tomllib.loads(path.read_text())
            if "project" in doc:
                self.assertEqual(doc["project"]["version"], version, path)

    def test_manifest_downloads_follow_repository_layout(self):
        prefix = "https://raw.githubusercontent.com/fmind/theme/main/"
        for path in ROOT.rglob("*.json"):
            if "node_modules" in path.parts:
                continue
            for target in re.findall(re.escape(prefix) + r'([^"\s]+)', path.read_text()):
                self.assertTrue((ROOT.parent / target).is_file(), f"{path}: {target}")

    def test_all_themes_and_palette_are_documented(self):
        readme = (ROOT.parent / "README.md").read_text()
        entries = re.findall(r"(?m)^- \[([^\]]+)\]\(themes/([^/]+)/\)$", readme)
        self.assertEqual(len(entries), len(APPS))
        self.assertEqual({slug for _, slug in entries}, {app.name for app in APPS})
        self.assertEqual(entries, sorted(entries, key=lambda entry: (entry[0].casefold(), entry[1])))
        for app in APPS:
            self.assertTrue((app / "README.md").is_file(), app)
        for color in PALETTE["official"] + PALETTE["custom"]:
            self.assertIn(color.lower(), readme.lower())

    def test_tool_readme_local_links(self):
        for app in APPS:
            parser = Links()
            parser.feed(markdown.markdown((app / "README.md").read_text(), extensions=["fenced_code", "tables"]))
            for target in parser.links + parser.images:
                url = urlsplit(target)
                if url.path and not url.scheme and not url.netloc:
                    self.assertTrue((app / unquote(url.path)).exists(), f"{app.name}: {target}")

    def test_repository_documentation_links_and_images(self):
        paths = [ROOT.parent / name for name in ("README.md", "AGENTS.md", "CHANGELOG.md")]
        paths += [ROOT.parent / folder / "README.md" for folder in ("artworks", "banners", "wallpapers")]
        for path in paths:
            parser = Links()
            parser.feed(markdown.markdown(path.read_text(), extensions=["fenced_code", "tables", "toc"]))
            for target in parser.links + parser.images:
                url = urlsplit(target)
                if url.scheme or url.netloc:
                    continue
                with self.subTest(document=path.name, target=target):
                    if url.path:
                        self.assertTrue((path.parent / unquote(url.path)).exists())
                    elif url.fragment:
                        self.assertIn(unquote(url.fragment), parser.ids)


class SharedTests(unittest.TestCase):
    def test_palette_contrast_and_preview(self):
        preview = (ROOT.parent / "screenshots/palette.svg").read_text().lower()
        for color in PALETTE["official"] + PALETTE["custom"]:
            self.assertIn(color, preview)
        for color in {PALETTE["text"], PALETTE["gutter"], *PALETTE["roles"].values(), *PALETTE["ansi"].values()}:
            with self.subTest(color=color):
                self.assertGreaterEqual(contrast(color, PALETTE["ground"]), 4.5)

    def test_structured_theme_files(self):
        # Honor ignored build/dependency directories and pending deletions.
        paths = subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", "themes"],
            cwd=ROOT.parent,
            text=True,
        ).split("\0")
        for name in sorted(set(paths) - {""}):
            path = ROOT.parent / name
            if not path.is_file():
                continue
            parser = {".json": json.loads, ".toml": tomllib.loads, ".yaml": yaml.safe_load, ".yml": yaml.safe_load}.get(
                path.suffix
            )
            if parser:
                with self.subTest(path=name):
                    parser(path.read_text())

    def test_artwork_manifest(self):
        artwork = ROOT.parent / "artworks"
        manifest = json.loads((artwork / "manifest.json").read_text())
        self.assertTrue((artwork / "OFL.txt").is_file())
        for name, digest in manifest["inputs"].items():
            with self.subTest(source=name):
                self.assertEqual(hashlib.sha256((artwork / name).read_bytes()).hexdigest(), digest)
        self.assertTrue(manifest["exports"])
        for record in manifest["exports"]:
            with self.subTest(export=record["file"]):
                data = (ROOT.parent / record["file"]).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), record["sha256"])
                self.assertEqual(len(data), record["bytes"])
                self.assertTrue((ROOT.parent / record["svg"]).is_file())
