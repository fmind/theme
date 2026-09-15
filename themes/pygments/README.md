# Fmind for Pygments

Files: [fmind.py](fmind.py).

## Installation

Configuration destinations are relative to `~/.config` unless an absolute path or another location is specified. Merge fragments into existing settings.

Copy the module into your Python project and pass `FmindStyle` to `HtmlFormatter`, as shown below. Requires Pygments; no changes to installed Pygments files.

With `fmind.py` beside your script:

```python
from pathlib import Path

from fmind import FmindStyle
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

source = Path("example.py").read_text()
html = highlight(source, PythonLexer(), HtmlFormatter(style=FmindStyle, full=True))
Path("example.html").write_text(html)
```
