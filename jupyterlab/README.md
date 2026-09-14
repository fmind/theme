# Fmind for JupyterLab and Notebook 7

This is a native prebuilt-extension package for JupyterLab 4.6.3+ and Jupyter Notebook 7.6+. Build a wheel from this source directory with Node.js/npm and uv installed:

```sh
uv build --wheel .
```

Install the resulting wheel into the Python environment that runs Jupyter:

```sh
python -m pip install dist/jupyterlab_fmind-1.0.0-py3-none-any.whl
```

Restart Jupyter and refresh the browser. In JupyterLab, choose Settings → Theme → Fmind. In Notebook 7, choose Settings → Theme → Fmind. The installed wheel contains the compiled frontend; end users installing a wheel do not need Node.js or a JupyterLab rebuild. The package registers Fmind without selecting it or changing preferences.

The theme covers the native CSS variable API, notebook cells, CodeMirror syntax, output, forms, dialogs, search, completions and UI states. It uses Google Sans for UI/text and Google Sans Code for code, with system fallbacks and no remote font requests. The terminal's inherited canvas follows the theme; xterm's built-in ANSI palette and application-supplied output colors remain outside this CSS theme's control.

For classic Notebook 6 or NbClassic, use the separate [classic Notebook port](../jupyter-notebook/README.md). The native variable vocabulary and dimensions retain Jupyter's BSD notice in `LICENSE`.

Build dependencies are locked in `package-lock.json`. The sanitize-html override selects the patched 2.17.7 release for the build graph; apputils is supplied by the host at runtime and is not bundled. This override does not patch the host Jupyter application. The transitive exenv-es6 package still emits an upstream deprecation notice on a fresh npm install.
