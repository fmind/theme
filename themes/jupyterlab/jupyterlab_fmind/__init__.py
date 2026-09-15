# https://jupyterlab.readthedocs.io/en/stable/extension/extension_dev.html#packaging-information
"""Discover the bundled Fmind frontend extension."""


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": "jupyterlab-fmind"}]
