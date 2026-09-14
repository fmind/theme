# https://github.com/thonny/thonny/wiki/Plugins
"""Fmind light UI, editor and shell themes; selected explicitly by the user."""

from thonny.plugins.clean_ui_themes import clean
from thonny.workbench import UiThemeSettings

from thonny import get_workbench

from .syntax import syntax


def ui() -> UiThemeSettings:
    settings = clean(
        frame_background="#ffffff",
        text_background="#ffffff",
        normal_detail="#ffffff",
        high_detail="#d2e3fc",
        low_detail="#f1f3f4",
        normal_foreground="#202124",
        high_foreground="#174ea6",
        low_foreground="#595d62",
    )
    # Correct the native helper's tooltip and demonstration slider colors.
    settings["Tip.TLabel"]["configure"].update(foreground="#202124", background="#ffffff")
    settings["Tip.TFrame"]["configure"].update(background="#ffffff")
    settings["TScale.slider"]["configure"].update(
        background="#174ea6", troughcolor="#ffffff", lightcolor="#174ea6", darkcolor="#174ea6"
    )
    settings["Gutter"]["configure"]["background"] = "#ffffff"
    settings["Url.TLabel"]["configure"]["foreground"] = "#174ea6"
    for name in ("Menubar", "Menu"):
        settings[name]["configure"].update(activebackground="#d2e3fc", activeforeground="#174ea6")
    settings["."]["configure"].update(font="TkDefaultFont", bordercolor="#9aa0a6")
    return settings


def load_plugin() -> None:
    workbench = get_workbench()
    workbench.add_ui_theme("Fmind", "Enhanced Clam", ui)
    workbench.add_syntax_theme("Fmind", "Default Light", syntax)
