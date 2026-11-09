# Fmind for JupyterLab and Notebook 7

Files: [LICENSE](LICENSE), [custom.css](custom.css).

Format: [JupyterLab custom CSS](https://jupyterlab.readthedocs.io/en/stable/user/custom_css.html) · [Notebook custom CSS](https://jupyter-notebook.readthedocs.io/en/stable/custom_css.html) · [JupyterLab CSS variables](https://jupyterlab.readthedocs.io/en/stable/developer/css.html#css-variables)

A user stylesheet that restyles the built-in JupyterLab Light theme. It needs no extension, package or build. Tested with JupyterLab 4.6.6 and Notebook 7.6.5.

## Installation

1. Copy `custom.css` to `custom/custom.css` in your Jupyter configuration directory (normally `~/.jupyter/`; run `jupyter --config-dir` to locate it). Preserve any existing custom CSS by combining the files, with Fmind's rules last.
2. JupyterLab loads custom CSS only when asked: start it with `jupyter lab --custom-css`, or add `c.LabApp.custom_css = True` to `jupyter_lab_config.py`. Notebook 7 loads it by default.
3. Restart Jupyter, refresh the browser and choose Settings → Theme → JupyterLab Light. Dark themes stay unchanged.

The stylesheet covers the native CSS variable API, notebook cells, CodeMirror syntax, output, forms, dialogs, search, completions and UI states. It uses Google Sans for UI/text and Google Sans Code for code, with system fallbacks and no remote font requests. The terminal's inherited canvas follows the theme; xterm's built-in ANSI palette and application-supplied output colors remain outside its control.

Classic Notebook 6 and NbClassic also read `custom/custom.css`, but they do not use JupyterLab's CSS variables, so this stylesheet does not theme them.

If you installed the `jupyterlab-fmind` extension from Fmind 6.x or earlier, remove it with `python -m pip uninstall jupyterlab-fmind`. The native variable vocabulary and dimensions retain Jupyter's BSD notice in `LICENSE`.
