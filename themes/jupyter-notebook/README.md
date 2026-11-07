# Fmind for Jupyter Notebook

Format: [NbClassic custom CSS path](https://github.com/jupyter/nbclassic/blob/main/nbclassic/notebookapp.py)

For **Notebook 7**, use the [JupyterLab port](../jupyterlab/README.md) instead.

For **classic Notebook 6 or NbClassic**, copy `custom.css` into `custom/custom.css` under your Jupyter configuration directory (normally `~/.jupyter/`). Run `jupyter --config-dir` to locate that directory. Preserve any existing custom CSS by combining the files, with Fmind's rules last. Restart or reload the notebook page. JupyterLab and Notebook 7 read the same file, and these global rules would restyle them too; keep the two ports in separate configuration directories with `JUPYTER_CONFIG_DIR`.

The classic stylesheet covers the file dashboard, navigation, forms, dialogs, notebook cells, output, Markdown, CodeMirror syntax, search, completions and status labels. It changes colors and fonts without replacing the notebook's layout. Install Google Sans and Google Sans Code locally; the theme makes no external font requests. Arbitrary HTML/plot output and application-provided ANSI colors can override the theme.
