# https://github.com/thonny/thonny/blob/master/thonny/plugins/base_syntax_themes.py
"""Pure editor and shell style definitions, independent of a running workbench."""


def syntax() -> dict[str, dict[str, str | int | bool]]:
    styles = {
        "TEXT": {"foreground": "#202124", "background": "#ffffff", "insertbackground": "#174ea6"},
        "GUTTER": {"foreground": "#595d62", "background": "#ffffff"},
        "sel": {"foreground": "#202124", "background": "#d2e3fc"},
        "current_line": {"background": "#f1f3f4"},
        "breakpoint": {"foreground": "#a50e0e"},
        "definition": {"foreground": "#174ea6", "font": "BoldEditorFont"},
        "class_definition": {"foreground": "#681da8", "font": "BoldEditorFont"},
        "function_definition": {"foreground": "#174ea6", "font": "BoldEditorFont"},
        "function_call": {"foreground": "#174ea6"},
        "method_call": {"foreground": "#174ea6"},
        "string": {"foreground": "#0d652d"},
        "string3": {"foreground": "#0d652d", "font": "EditorFont"},
        "open_string": {"foreground": "#a50e0e", "background": "#fad2cf"},
        "open_string3": {"foreground": "#a50e0e", "background": "#fad2cf", "font": "EditorFont"},
        "tab": {"background": "#f1f3f4"},
        "keyword": {"foreground": "#174ea6", "font": "BoldEditorFont"},
        "builtin": {"foreground": "#681da8"},
        "number": {"foreground": "#934900"},
        "comment": {"foreground": "#595d62"},
        "welcome": {"foreground": "#595d62"},
        "magic": {"foreground": "#681da8"},
        "prompt": {"foreground": "#174ea6", "font": "BoldIOFont"},
        "stdin": {"foreground": "#202124"},
        "stdout": {"foreground": "#202124"},
        "stderr": {"foreground": "#a50e0e"},
        "value": {"foreground": "#934900"},
        "hyperlink": {"foreground": "#174ea6", "underline": True},
        "name_link": {"foreground": "#174ea6", "underline": True},
        "surrounding_parens": {"foreground": "#174ea6", "background": "#d2e3fc", "font": "BoldEditorFont"},
        "unclosed_expression": {"background": "#fad2cf"},
        "found": {"foreground": "#202124", "background": "#feefc3", "underline": True},
        "current_found": {"foreground": "#934900", "background": "#feefc3", "underline": True},
        "matched_name": {"background": "#d2e3fc"},
        "local_name": {"foreground": "#202124", "font": "EditorFont"},
        "active_focus": {"background": "#d2e3fc", "borderwidth": 1, "relief": "solid"},
        "suspended_focus": {"background": "#feefc3", "borderwidth": 1, "relief": "solid"},
        "completed_focus": {"background": "#ceead6", "borderwidth": 1, "relief": "flat"},
        "exception_focus": {"foreground": "#a50e0e", "background": "#fad2cf", "borderwidth": 1, "relief": "solid"},
        "expression_box": {"foreground": "#202124", "background": "#ffffff"},
    }
    # Shell ANSI backgrounds are pale so inherited syntax remains readable.
    ansi = {
        "black": ("#202124", "#f1f3f4"),
        "red": ("#a50e0e", "#fad2cf"),
        "green": ("#0d652d", "#ceead6"),
        "yellow": ("#934900", "#feefc3"),
        "blue": ("#174ea6", "#d2e3fc"),
        "magenta": ("#681da8", "#d2e3fc"),
        "cyan": ("#00636d", "#d2e3fc"),
        "white": ("#202124", "#ffffff"),
        "fore": ("#202124", "#f1f3f4"),
        "back": ("#202124", "#ffffff"),
    }
    for name, (foreground, background) in ansi.items():
        for prefix in ("", "bright_", "dim_"):
            styles[prefix + name + "_fg"] = {"foreground": foreground}
            styles[prefix + name + "_bg"] = {"background": background}
    styles.update(
        {
            "intense_io": {"font": "BoldIOFont"},
            "italic_io": {"font": "IOFont"},
            "intense_italic_io": {"font": "BoldIOFont"},
            "underline": {"underline": True},
            "strikethrough": {"overstrike": True},
        }
    )
    return styles
