"""Check release metadata, theme files, the theme index and documentation navigation."""

import functools
import hashlib
import json
import plistlib
import re
import subprocess
import tomllib
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1] / "themes"
APPS = sorted(path for path in ROOT.iterdir() if path.is_dir() and not path.name.startswith((".", "__")))
PALETTE = yaml.safe_load((ROOT.parent / "checks/palette.yaml").read_text())
DESIGN = yaml.safe_load((ROOT.parent / "DESIGN.md").read_text().split("---\n")[1])
COLORS = {*PALETTE["official"], *PALETTE["custom"]}
# XML files without an XML declaration; other XML and JSON files are recognized by their content.
XML_SUFFIXES = {".icls", ".qrc", ".svg", ".vssettings", ".xaml", ".xml"}
# Hex colors as #rrggbb, #rrggbbaa or #aarrggbb. Short forms are skipped: anchors, issue numbers and CSS IDs match them.
HEX = re.compile(r"(?<![\w&#/])#([0-9a-f]{6}|[0-9a-f]{8})(?![\w-])", re.IGNORECASE)
# Release versions are X.Y.Z; native format and API versions such as 2, "1" or 1.0 are ignored.
SEMVER = re.compile(r"\d+\.\d+\.\d+")
TEXT_VERSIONS = {
    ".css": re.compile(r"(?m)^\s*\*?\s*@version\s+(\S+)"),
    ".desktop": re.compile(r"(?m)^(?:X-KDE-PluginInfo-)?Version=(\S+)$"),
}


def files(*pathspecs):
    """Return tracked and untracked files, honoring ignored build directories and pending deletions."""
    names = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", *pathspecs],
        cwd=ROOT.parent,
        text=True,
    ).split("\0")
    return [path for name in sorted(set(names) - {""}) if (path := ROOT.parent / name).is_file()]


@functools.cache
def theme_texts():
    """Return (path, text) for every UTF-8 file under themes/, skipping binary assets."""
    texts = []
    for path in files("themes"):
        try:
            texts.append((path, path.read_text(encoding="utf-8")))
        except UnicodeDecodeError:
            continue
    return tuple(texts)


def is_json(path, text):
    """Recognize JSON by suffix or, for app-specific suffixes, by a top-level object."""
    suffix = path.suffix.lower()
    # JSONC may legitimately hold comments, and YAML flow mappings also start with a brace.
    if suffix in (".jsonc", ".toml", ".yaml", ".yml"):
        return False
    return suffix == ".json" or (text.lstrip().startswith("{") and text.rstrip().endswith("}"))


def parse(path, text):
    """Parse a structured file by suffix or unambiguous content; return None for other formats."""
    suffix = path.suffix.lower()
    if suffix == ".toml":
        return tomllib.loads(text)
    if suffix in (".yaml", ".yml"):
        return yaml.safe_load(text)
    if is_json(path, text):
        return json.loads(text)
    if suffix in XML_SUFFIXES or text.lstrip().startswith("<?xml"):
        data = path.read_bytes()
        element = ET.fromstring(data)
        return plistlib.loads(data) if element.tag == "plist" else element
    return None


def strings(node):
    """Yield every string in a parsed YAML tree."""
    if isinstance(node, str):
        yield node
    elif isinstance(node, (dict, list)):
        for value in node.values() if isinstance(node, dict) else node:
            yield from strings(value)


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


@functools.cache
def links(path):
    """Return the links, images and anchors of a rendered Markdown file."""
    parser = Links()
    parser.feed(markdown.markdown(path.read_text(), extensions=["fenced_code", "tables", "toc"]))
    return parser


class DocumentationTests(unittest.TestCase):
    def test_release_versions_are_consistent(self):
        version = tomllib.loads((ROOT.parent / "pyproject.toml").read_text())["project"]["version"]
        for path, text in theme_texts():
            if pattern := TEXT_VERSIONS.get(path.suffix):
                found = pattern.findall(text)
            elif path.name == "pyproject.toml":
                found = [tomllib.loads(text).get("project", {}).get("version")]
            elif is_json(path, text) and isinstance(doc := json.loads(text), dict):
                # Package, extension and theme metadata; a lockfile repeats its root package version.
                found = [doc.get("version"), doc.get("theme_version"), doc.get("KPlugin", {}).get("Version")]
                if path.name == "package-lock.json":
                    found.append(doc["packages"][""]["version"])
            else:
                continue
            for value in found:
                if isinstance(value, str) and SEMVER.fullmatch(value):
                    self.assertEqual(value, version, path)

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
        for color in COLORS:
            self.assertIn(color.lower(), readme.lower())

    def test_theme_readmes_cite_their_format(self):
        # AGENTS.md keeps a port only while its README cites the upstream format or loader.
        cited = re.compile(r"(?m)^Format: .*\]\(https://[^)\s]+\)")
        missing = [app.name for app in APPS if not cited.search((app / "README.md").read_text())]
        self.assertEqual(missing, [])

    def test_markdown_local_links_and_anchors(self):
        # Screenshot samples are rendering fixtures, not navigation.
        for path in files("*.md", ":!screenshots/samples"):
            document = links(path)
            for target in document.links + document.images:
                url = urlsplit(target)
                if url.scheme or url.netloc:
                    continue
                with self.subTest(document=str(path.relative_to(ROOT.parent)), target=target):
                    resolved = (path.parent / unquote(url.path)).resolve() if url.path else path
                    self.assertTrue(resolved.exists())
                    # A directory link opens its README on GitHub, so its anchors come from there.
                    anchors = resolved / "README.md" if resolved.is_dir() else resolved
                    if url.fragment and anchors.suffix == ".md":
                        self.assertIn(unquote(url.fragment), links(anchors).ids)


class SharedTests(unittest.TestCase):
    def test_palette_contrast_and_preview(self):
        preview = (ROOT.parent / "screenshots/palette.svg").read_text().lower()
        for color in COLORS:
            self.assertIn(color, preview)
        listed = {value.lower() for value in strings(PALETTE) if re.fullmatch(r"#[0-9a-fA-F]{6}", value)}
        self.assertLessEqual(listed, COLORS)
        for color in {PALETTE["text"], PALETTE["gutter"], *PALETTE["roles"].values(), *PALETTE["ansi"].values()}:
            with self.subTest(color=color):
                self.assertGreaterEqual(contrast(color, PALETTE["ground"]), 4.5)

    def test_design_tokens_match_palette(self):
        colors = {name: value.lower() for name, value in DESIGN["colors"].items()}
        self.assertEqual(set(colors.values()), COLORS)
        self.assertEqual(len(colors), len(set(colors.values())))
        for name, tokens in DESIGN["components"].items():
            values = {
                key: colors[value[len("{colors.") : -1]]
                for key, value in tokens.items()
                if value.startswith("{colors.")
            }
            if {"backgroundColor", "textColor"} <= values.keys():
                with self.subTest(component=name):
                    self.assertGreaterEqual(contrast(values["textColor"], values["backgroundColor"]), 4.5)

    def test_design_token_references_resolve(self):
        for value in strings(DESIGN):
            if reference := re.fullmatch(r"\{([\w.-]+)\}", value):
                with self.subTest(reference=value):
                    node = DESIGN
                    for key in reference[1].split("."):
                        self.assertIsInstance(node, dict)
                        self.assertIn(key, node)
                        node = node[key]

    def test_structured_theme_files(self):
        for path, text in theme_texts():
            with self.subTest(path=str(path.relative_to(ROOT.parent))):
                parse(path, text)

    def test_theme_colors_are_palette_colors(self):
        # 0x, decimal and Windows BGR color encodings are not checked.
        off_palette = []
        for path, text in theme_texts():
            for value in HEX.findall(text):
                # An 8-digit value is #rrggbbaa or #aarrggbb, so either 6-digit part may hold the color.
                if not {"#" + value[:6].lower(), "#" + value[-6:].lower()} & COLORS:
                    off_palette.append(f"{path.relative_to(ROOT.parent)}: #{value}")
        self.assertEqual(off_palette, [])

    def test_hex_colors_skip_anchors_and_references(self):
        text = "[Add the theme](#add-the-theme), [Decade](#decade-notes), issue #123, #feed, `#174EA6`, '#80fbbc04'"
        self.assertEqual(HEX.findall(text), ["174EA6", "80fbbc04"])

    def test_kde_color_scheme_copies_match(self):
        # themes/gtk/kde/README.md requires these copies of the application scheme to stay identical.
        kde = ROOT / "gtk/kde"
        scheme = (kde / "color-schemes/Fmind.colors").read_bytes()
        for copy in ("kvantum/Fmind/Fmind.colors", "plasma/look-and-feel/Fmind/contents/colors"):
            with self.subTest(copy=copy):
                self.assertEqual((kde / copy).read_bytes(), scheme)

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
