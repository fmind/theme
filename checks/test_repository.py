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

ROOT = Path(__file__).resolve().parents[1]
THEMES = ROOT / "themes"
APPS = sorted(path for path in THEMES.iterdir() if path.is_dir() and not path.name.startswith((".", "__")))
PALETTE = yaml.safe_load((ROOT / "checks/palette.yaml").read_text())
DESIGN = yaml.safe_load((ROOT / "DESIGN.md").read_text().split("---\n")[1])
COLORS = {*PALETTE["official"], *PALETTE["custom"]}
# XML files without an XML declaration; other XML and JSON files are recognized by their content.
XML_SUFFIXES = {".icls"}
# Hex colors as #rrggbb, #rrggbbaa or #aarrggbb. Short forms are skipped: anchors, issue numbers and CSS IDs match them.
HEX = re.compile(r"(?<![\w&#/])#([0-9a-f]{6}|[0-9a-f]{8})(?![\w-])", re.IGNORECASE)
# Truecolor ANSI SGR sequences (38 foreground, 48 background, 58 underline) in semicolon or ISO-8613-6 colon form.
SGR_RGB = re.compile(r"(?<!\d)(?:38|48|58)(?:;2;|:2::?)(\d{1,3})[;:](\d{1,3})[;:](\d{1,3})(?!\d)")
# Standard 16-color and attribute SGR parameters valid in .dircolors, LS_COLORS, GREP_COLORS and JQ_COLORS.
SGR_CODES = {
    0,
    1,
    2,
    3,
    4,
    5,
    7,
    8,
    9,
    *range(22, 30),
    *range(30, 38),
    39,
    *range(40, 48),
    49,
    *range(90, 98),
    *range(100, 108),
}
DIRCOLORS_KEYWORDS = {"COLOR", "COLORTERM", "EIGHTBIT", "OPTIONS", "TERM"}
SGR_ENV = re.compile(r"\b(LS_COLORS|GREP_COLORS|JQ_COLORS)=['\"]([^'\"]+)['\"]")
# Release versions are X.Y.Z; native format and API versions such as 2, "1" or 1.0 are ignored.
SEMVER = re.compile(r"\d+\.\d+\.\d+")


def bad_sgr(seq: str) -> list[str]:
    """Return off-palette RGB triplets or invalid SGR codes (such as bare R;G;B or 38;5;N) in an SGR parameter string."""
    if not seq:
        return []
    parts = seq.split(";")
    invalid = []
    index = 0
    while index < len(parts):
        if not parts[index].isdigit():
            return [seq]
        code = int(parts[index])
        if (
            code in (38, 48, 58)
            and index + 4 < len(parts)
            and parts[index + 1] == "2"
            and all(part.isdigit() for part in parts[index + 2 : index + 5])
        ):
            channels = tuple(int(part) for part in parts[index + 2 : index + 5])
            value = f"#{channels[0]:02x}{channels[1]:02x}{channels[2]:02x}"
            if any(channel > 255 for channel in channels) or value not in COLORS:
                invalid.append(f"{channels[0]};{channels[1]};{channels[2]}")
            index += 5
        elif code in SGR_CODES:
            index += 1
        else:
            invalid.append(seq)
            break
    return invalid


def files(*pathspecs):
    """Return tracked and untracked files, honoring ignored build directories and pending deletions."""
    names = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", *pathspecs],
        cwd=ROOT,
        text=True,
    ).split("\0")
    return [path for name in sorted(set(names) - {""}) if (path := ROOT / name).is_file()]


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
        version = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["version"]
        for path, text in theme_texts():
            # Extension and browser theme manifests carry the release version.
            if is_json(path, text) and isinstance(doc := json.loads(text), dict):
                value = doc.get("version")
                if isinstance(value, str) and SEMVER.fullmatch(value):
                    self.assertEqual(value, version, path)

    def test_all_themes_and_palette_are_documented(self):
        readme = (ROOT / "README.md").read_text()
        catalog = readme.split("\n## Available themes\n")[1].split("\n## ")[0]
        ports = []
        for category in catalog.split("\n### ")[1:]:
            # A category lists its apps alphabetically; `#section` entries share another port's files.
            names = re.findall(r"(?m)^- \[([^\]]+)\]\(themes/[^)]+\)$", category)
            self.assertEqual(names, sorted(names, key=str.casefold), category.splitlines()[0])
            ports += re.findall(r"(?m)^- \[[^\]]+\]\(themes/([^/]+)/\)$", category)
        # Every port is listed exactly once.
        self.assertEqual(sorted(ports), [app.name for app in APPS])
        for app in APPS:
            self.assertTrue((app / "README.md").is_file(), app)
        for color in COLORS:
            self.assertIn(color.lower(), readme.lower())

    def test_design_md_commands_use_the_pinned_version(self):
        # Consumers run design.md through npx; maintainers run the version mise.toml pins.
        pin = tomllib.loads((ROOT / "mise.toml").read_text())["tools"]["npm:@google/design.md"]
        versions = {
            version
            for path in files("*.md")
            for version in re.findall(r"@google/design\.md@([\w.-]+)", path.read_text())
        }
        self.assertEqual(versions, {pin})

    def test_theme_readmes_share_one_layout(self):
        # AGENTS.md keeps a port only while its README cites the upstream format or loader.
        cited = re.compile(r"(?m)^Format: .*\]\(https://[^)\s]+\)")
        for app in APPS:
            readme = (app / "README.md").read_text()
            with self.subTest(app=app.name):
                self.assertTrue(readme.startswith("# Fmind for "))
                self.assertRegex(readme, cited)
                self.assertIn("\n## Installation\n", readme)
                # The `Files:` line links every file of the port.
                listed = re.search(r"(?m)^Files: (.*)$", readme)
                self.assertIsNotNone(listed)
                linked = set(re.findall(r"\]\(([^)]+)\)", listed.group(1)))
                shipped = {str(path.relative_to(app)) for path in files(f"themes/{app.name}")} - {"README.md"}
                self.assertEqual(linked, shipped)

    def test_markdown_local_links_and_anchors(self):
        # Screenshot samples are rendering fixtures, not navigation.
        for path in files("*.md", ":!screenshots/samples"):
            document = links(path)
            for target in document.links + document.images:
                url = urlsplit(target)
                if url.scheme or url.netloc:
                    continue
                with self.subTest(document=str(path.relative_to(ROOT)), target=target):
                    resolved = (path.parent / unquote(url.path)).resolve() if url.path else path
                    self.assertTrue(resolved.exists())
                    # A directory link opens its README on GitHub, so its anchors come from there.
                    anchors = resolved / "README.md" if resolved.is_dir() else resolved
                    if url.fragment and anchors.suffix == ".md":
                        self.assertIn(unquote(url.fragment), links(anchors).ids)


class SharedTests(unittest.TestCase):
    def test_palette_contrast_and_preview(self):
        preview = (ROOT / "screenshots/palette.svg").read_text().lower()
        for color in COLORS:
            self.assertIn(color, preview)
        listed = {value.lower() for value in strings(PALETTE) if re.fullmatch(r"#[0-9a-fA-F]{6}", value)}
        self.assertLessEqual(listed, COLORS)
        for color in {PALETTE["text"], PALETTE["gutter"], *PALETTE["roles"].values(), *PALETTE["ansi"].values()}:
            with self.subTest(color=color):
                self.assertGreaterEqual(contrast(color, PALETTE["ground"]), 4.5)

    def test_design_tokens_match_palette(self):
        # `mise run check:design` lints token references and component contrast.
        colors = [value.lower() for value in DESIGN["colors"].values()]
        self.assertEqual(set(colors), COLORS)
        self.assertEqual(len(colors), len(set(colors)))

    def test_structured_theme_files(self):
        for path, text in theme_texts():
            with self.subTest(path=str(path.relative_to(ROOT))):
                parse(path, text)

    def test_theme_colors_are_palette_colors(self):
        # 0x, decimal and Windows BGR color encodings are not checked.
        off_palette = []
        for path, text in theme_texts():
            for value in HEX.findall(text):
                # An 8-digit value is #rrggbbaa or #aarrggbb, so either 6-digit part may hold the color.
                if not {"#" + value[:6].lower(), "#" + value[-6:].lower()} & COLORS:
                    off_palette.append(f"{path.relative_to(ROOT)}: #{value}")
            for red, green, blue in SGR_RGB.findall(text):
                channels = (int(red), int(green), int(blue))
                value = f"#{channels[0]:02x}{channels[1]:02x}{channels[2]:02x}"
                if any(channel > 255 for channel in channels) or value not in COLORS:
                    off_palette.append(f"{path.relative_to(ROOT)}: {red};{green};{blue}")
            if path.name == ".dircolors":
                for line in text.splitlines():
                    if line.strip() and not line.lstrip().startswith("#"):
                        key, sgr = line.split(None, 1)
                        if key not in DIRCOLORS_KEYWORDS:
                            off_palette += [f"{path.relative_to(ROOT)}: {item}" for item in bad_sgr(sgr)]
            for var, raw in SGR_ENV.findall(text):
                for entry in raw.split(":"):
                    if entry:
                        sgr = entry.split("=", 1)[-1] if var != "JQ_COLORS" else entry
                        off_palette += [f"{path.relative_to(ROOT)}: {item}" for item in bad_sgr(sgr)]
        self.assertEqual(off_palette, [])

    def test_ports_do_not_share_identical_files(self):
        # An identical theme file in two ports is a variant: keep one port and add the other app to its README.
        ports = {}
        for path in files("themes"):
            if path.name != "LICENSE":
                ports.setdefault(hashlib.sha256(path.read_bytes()).hexdigest(), set()).add(
                    path.relative_to(THEMES).parts[0]
                )
        self.assertEqual([sorted(shared) for shared in ports.values() if len(shared) > 1], [])

    def test_hex_colors_skip_anchors_and_references(self):
        text = "[Add the theme](#add-the-theme), [Decade](#decade-notes), issue #123, #feed, `#174EA6`, '#80fbbc04'"
        self.assertEqual(HEX.findall(text), ["174EA6", "80fbbc04"])

    def test_sgr_and_ls_colors_validation(self):
        sample = "ms=01;38;2;32;33;36;48;2;254;239;195:fn=38:2::23:78:166"
        self.assertEqual(SGR_RGB.findall(sample), [("32", "33", "36"), ("254", "239", "195"), ("23", "78", "166")])
        self.assertEqual(bad_sgr("01;04;31"), [])
        self.assertEqual(bad_sgr("01;38;2;23;78;166;48;2;254;239;195"), [])
        self.assertEqual(bad_sgr("23;78;166"), ["23;78;166"])
        self.assertEqual(bad_sgr("38;5;196"), ["38;5;196"])
        self.assertEqual(bad_sgr("01;38;2;1;2;3"), ["1;2;3"])

    def test_artwork_manifest(self):
        artwork = ROOT / "artworks"
        manifest = json.loads((artwork / "manifest.json").read_text())
        self.assertTrue((artwork / "OFL.txt").is_file())
        for name, digest in manifest["inputs"].items():
            with self.subTest(source=name):
                self.assertEqual(hashlib.sha256((artwork / name).read_bytes()).hexdigest(), digest)
        self.assertTrue(manifest["exports"])
        for record in manifest["exports"]:
            with self.subTest(export=record["file"]):
                data = (ROOT / record["file"]).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), record["sha256"])
                self.assertEqual(len(data), record["bytes"])
                self.assertTrue((ROOT / record["svg"]).is_file())
