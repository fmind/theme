# Fmind for ptpython

Files: [fmind.py](fmind.py).

## Installation

Configuration destinations are relative to `~/.config` unless an absolute path or another location is specified. Merge fragments into existing settings.

Load `CODE` and `UI` in `config.py`; register and select them as shown below.

Place `fmind.py` in `~/.config/ptpython/` and add this inside your `configure(repl)` function. Adjust the explicit path if you use a different config directory; ptpython executes `config.py` without defining `__file__`.

```python
from pathlib import Path
from runpy import run_path

from prompt_toolkit.styles import Style

styles = run_path(str(Path("~/.config/ptpython/fmind.py").expanduser()))
repl.install_code_colorscheme("fmind", Style.from_dict(styles["CODE"]))
repl.install_ui_colorscheme("fmind", Style.from_dict(styles["UI"]))
repl.use_code_colorscheme("fmind")
repl.use_ui_colorscheme("fmind")
```
