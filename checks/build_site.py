"""Build a single static page from README; native downloads stay on GitHub."""

import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / ".cache/site"
REPOSITORY = "https://github.com/fmind/theme/blob/main/"


def render(source: str) -> str:
    def link(match: re.Match[str]) -> str:
        label, target = match.groups()
        if "://" not in target and not target.startswith(("#", "mailto:", "screenshots/")):
            target = REPOSITORY + target
        return f"[{label}]({target})"

    content = markdown.markdown(
        re.sub(r"\[([^\]]*)\]\(([^)]+)\)", link, source), extensions=["tables", "fenced_code", "toc"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Fmind: a practical light theme using the Google News palette.">
<title>Fmind — a practical light theme</title>
<link rel="icon" href="data:,">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;600&amp;family=Google+Sans+Code&amp;display=swap">
<style>
:root {{ color-scheme: light; font-family: "Google Sans", sans-serif; color: #202124; background: #ffffff; }}
body {{ max-width: 72rem; margin: auto; padding: 1.5rem; line-height: 1.6; }}
a {{ color: #174ea6; text-underline-offset: .2em; }}
a:focus-visible {{ outline: 2px solid #174ea6; outline-offset: 3px; }}
h1, h2, h3 {{ line-height: 1.25; margin-top: 2rem; }}
code, pre {{ font-family: "Google Sans Code", monospace; background: #f1f3f4; }}
code {{ overflow-wrap: anywhere; }}
pre {{ padding: 1rem; overflow-x: auto; }}
pre code {{ overflow-wrap: normal; }}
img {{ max-width: 100%; height: auto; }}
table {{ display: block; max-width: 100%; overflow-x: auto; border-collapse: collapse; margin: 1rem 0; }}
th, td {{ text-align: left; padding: .6rem; border-bottom: 1px solid #9aa0a6; min-width: 8rem; }}
th {{ background: #f1f3f4; }}
blockquote {{ margin-left: 0; padding-left: 1rem; border-left: 4px solid #595d62; }}
::selection {{ color: #202124; background: #d2e3fc; }}
</style>
</head>
<body><main>{content}</main></body>
</html>
"""


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "index.html").write_text(render((ROOT / "README.md").read_text()))
    (OUTPUT / "screenshots").mkdir(exist_ok=True)
    for name in ("palette.svg", "zellij.png", "markdown.png"):
        shutil.copyfile(ROOT / "screenshots" / name, OUTPUT / "screenshots" / name)
    print("Built .cache/site/index.html")


if __name__ == "__main__":
    main()
