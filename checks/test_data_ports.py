"""Notebook and data IDE package boundaries, syntax roles and highlighted text."""

import ast
import json
import re
import runpy
import tomllib
import unittest

import tinycss2
from test_theme import PALETTE, ROOT, contrast

COLORS = set(PALETTE["official"] + PALETTE["custom"])
SURFACES = {"#ffffff", "#f1f3f4", "#d2e3fc", "#ceead6", "#fad2cf", "#feefc3"}


def declarations(source):
    rules = {}
    for rule in tinycss2.parse_stylesheet(source, skip_comments=True, skip_whitespace=True):
        if rule.type != "qualified-rule":
            raise ValueError(f"Unexpected CSS rule: {rule.type}")
        selector = tinycss2.serialize(rule.prelude).strip()
        values = {}
        for d in tinycss2.parse_declaration_list(rule.content, skip_comments=True, skip_whitespace=True):
            if d.type != "declaration":
                raise ValueError(f"Invalid declaration in {selector}: {d.type}")
            values[d.name] = tinycss2.serialize(d.value).strip()
        rules[selector] = values
    return rules


class DataPortTests(unittest.TestCase):
    def readable(self, fg, bg, label):
        self.assertIn(fg, COLORS, label)
        self.assertIn(bg, COLORS, label)
        self.assertGreaterEqual(contrast(fg, bg), 4.5, label)

    def test_matlab_current_language_coverage_and_highlights(self):
        theme = json.loads((ROOT / "matlab/fmind.json").read_text())
        self.assertEqual(theme["DesktopTheme"], "Light")
        self.assertEqual(theme["BackgroundColor"], "#ffffff")
        self.assertEqual(
            set(theme["OtherLanguages"]),
            {
                "C",
                "Cpp",
                "XML",
                "HTML",
                "Simscape",
                "Java",
                "Javascript",
                "Markdown",
                "Typescript",
                "JSON",
                "Python",
                "YAML",
                "TLC",
                "Verilog",
                "VHDL",
            },
        )

        def walk(value):
            for key, item in value.items():
                self.assertNotEqual(key, "ApplySmartIndentWhileTyping")
                if isinstance(item, dict):
                    walk(item)
                elif isinstance(item, str) and item.startswith("#"):
                    self.assertIn(item, COLORS, key)
                    if key not in {
                        "BackgroundColor",
                        "RightHandTextLimitLineColor",
                        "HorizontalRuleColor",
                        "HighlightCurrentLineColor",
                        "AutofixHighlightColor",
                        "AutomaticallyHighlightColor",
                    }:
                        for bg in SURFACES:
                            self.readable(item, bg, key)

        walk(theme)
        python = theme["OtherLanguages"]["Python"]
        self.assertEqual(python["KeywordsColor"], "#174ea6")
        self.assertEqual(python["StringsColor"], "#0d652d")
        self.assertEqual(python["CommentsColor"], "#595d62")

    def test_matlab_legacy_signed_java_rgb(self):
        lines = (ROOT / "matlab/fmind.prf").read_text().splitlines()
        pairs = [line.split("=", 1) for line in lines if line and not line.startswith("#")]
        values = dict(pairs)
        self.assertEqual(len(pairs), len(values))
        self.assertEqual(values["ColorsUseSystem"], "Bfalse")
        colors = {}
        for key, value in values.items():
            if value.startswith("C"):
                number = int(value[1:])
                self.assertTrue(-(1 << 24) <= number < 0)
                colors[key] = f"#{number & 0xFFFFFF:06x}"
                self.assertIn(colors[key], COLORS)
            else:
                self.assertIn(value, ("Btrue", "Bfalse"))
        self.assertEqual(len(colors), 18)
        self.assertEqual(colors["ColorsBackground"], "#ffffff")
        self.readable(colors["ColorsText"], colors["ColorsBackground"], "MATLAB canvas")
        for key in ("Colors_M_Keywords", "Colors_M_Comments", "Colors_M_Strings", "Colors_M_Errors"):
            for bg in SURFACES:
                self.readable(colors[key], bg, key)

    def test_thonny_syntax_and_ansi_without_a_workbench(self):
        # Evaluate only the pure theme factory; the gate never starts or configures Thonny.
        tree = ast.parse((ROOT / "thonny/thonnycontrib/fmind/__init__.py").read_text())
        styles = runpy.run_path(str(ROOT / "thonny/thonnycontrib/fmind/syntax.py"))["syntax"]()
        self.assertEqual(len(styles), 104)
        for name, style in styles.items():
            fg = style.get("foreground", "#202124")
            bg = style.get("background", "#ffffff")
            self.readable(fg, bg, name)
            for surface in SURFACES:
                self.readable(fg, surface, name)
        self.assertEqual(styles["class_definition"]["foreground"], PALETTE["roles"]["type"])
        self.assertEqual(styles["function_call"]["foreground"], PALETTE["roles"]["function"])
        for prefix in ("", "bright_", "dim_"):
            for color in ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"):
                self.readable(
                    styles[prefix + color + "_fg"]["foreground"],
                    styles[prefix + color + "_bg"]["background"],
                    prefix + color,
                )
        plugin = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "load_plugin")
        calls = [
            node for node in ast.walk(plugin) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        ]
        self.assertEqual({node.func.attr for node in calls}, {"add_ui_theme", "add_syntax_theme"})

    def test_jupyter_native_variables_and_readable_states(self):
        rules = declarations((ROOT / "jupyterlab/style/index.css").read_text())
        variables = rules[":root"]
        self.assertEqual(len(variables), 221)

        def resolve(name):
            seen = set()
            value = variables["--jp-" + name]
            while value.startswith("var("):
                self.assertNotIn(value, seen)
                seen.add(value)
                value = variables[value[4:-1]]
            return value

        for name, value in variables.items():
            self.assertNotIn("--md-", value, name)
            if name.startswith("--jp-mirror-editor-"):
                for bg in SURFACES:
                    self.readable(value, bg, name)
        for i in range(3):
            self.assertEqual(resolve(f"layout-color{i}"), "#ffffff")
        for i in range(4):
            self.readable(resolve(f"ui-font-color{i}"), resolve("layout-color1"), "UI text")
            self.readable(resolve(f"ui-inverse-font-color{i}"), resolve("brand-color1"), "filled control")
        for name in ("accept", "warn", "reject"):
            for state in ("normal", "hover", "active"):
                self.readable("#ffffff", resolve(name + "-color-" + state), name)
        for selected in ("selected", "unselected"):
            self.readable(
                resolve(f"search-{selected}-match-color"),
                resolve(f"search-{selected}-match-background-color"),
                selected,
            )
        self.assertIn("Google Sans", resolve("ui-font-family"))
        self.assertIn("Google Sans Code", resolve("code-font-family-default"))

    def test_jupyter_prebuilt_package_and_theme_lifecycle(self):
        package = json.loads((ROOT / "jupyterlab/package.json").read_text())
        config = tomllib.loads((ROOT / "jupyterlab/pyproject.toml").read_text())
        self.assertEqual(package["name"], config["project"]["name"])
        self.assertEqual(package["version"], config["project"]["version"])
        self.assertTrue((ROOT / "jupyterlab" / package["main"]).is_file())
        self.assertTrue((ROOT / "jupyterlab" / package["jupyterlab"]["themePath"]).is_file())
        self.assertNotIn("style", package)
        self.assertNotIn("styleModule", package)
        source = (ROOT / "jupyterlab" / package["main"]).read_text()
        self.assertIn("isLight: true", source)
        self.assertIn("manager.loadCSS('jupyterlab-fmind/index.css')", source)
        self.assertIn("unload: () => Promise.resolve()", source)
        self.assertNotIn("setTheme", source)
        lock = json.loads((ROOT / "jupyterlab/package-lock.json").read_text())
        self.assertEqual(lock["packages"][""]["version"], package["version"])
        self.assertEqual(lock["packages"][""]["devDependencies"], package["devDependencies"])
        for entry in lock["packages"].values():
            if "resolved" in entry:
                self.assertTrue(entry["resolved"].startswith("https://registry.npmjs.org/"))

    def test_classic_notebook_syntax_controls_and_no_remote_assets(self):
        source = (ROOT / "jupyter-notebook/custom.css").read_text()
        rules = declarations(source)
        self.assertGreater(len(rules), 60)
        self.assertNotRegex(re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL), r"url\(|@import")
        for selector, values in rules.items():
            if "color" in values:
                bg = values.get("background", "#ffffff")
                self.readable(values["color"], bg, selector)
                if "cm-s-ipython" in selector:
                    for surface in SURFACES:
                        self.readable(values["color"], surface, selector)
        for kind in ("comment", "string", "number", "error"):
            self.assertTrue(any(".cm-" + kind in selector for selector in rules), kind)
