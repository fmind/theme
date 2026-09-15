# https://pygments.org/docs/styles/#creating-own-styles
"""Fmind light Pygments style; load with HtmlFormatter."""

from typing import ClassVar

from pygments.style import Style
from pygments.token import Comment, Error, Generic, Keyword, Literal, Name, Number, Operator, Punctuation, String, Text


class FmindStyle(Style):
    name = "Fmind"
    background_color = "#ffffff"
    highlight_color = "#d2e3fc"
    line_number_color = "#595d62"
    line_number_background_color = "#ffffff"
    line_number_special_color = "#202124"
    line_number_special_background_color = "#d2e3fc"
    styles: ClassVar[dict[tuple[str, ...], str]] = {
        Text: "#202124",
        Text.Whitespace: "#595d62",
        Comment: "#595d62",
        Comment.Preproc: "#681da8",
        Keyword: "bold #174ea6",
        Keyword.Type: "#681da8",
        Name: "#202124",
        Name.Builtin: "#681da8",
        Name.Class: "#681da8",
        Name.Namespace: "#681da8",
        Name.Function: "#174ea6",
        Name.Decorator: "#681da8",
        Name.Constant: "#934900",
        Name.Tag: "#174ea6",
        Name.Exception: "#a50e0e",
        Literal: "#934900",
        String: "#0d652d",
        String.Escape: "#174ea6",
        Number: "#934900",
        Operator: "#202124",
        Operator.Word: "bold #174ea6",
        Punctuation: "#202124",
        Generic: "#202124",
        Generic.Deleted: "#a50e0e bg:#fad2cf",
        Generic.Inserted: "#0d652d bg:#ceead6",
        Generic.Error: "#a50e0e",
        Generic.Traceback: "#a50e0e",
        Generic.Heading: "bold #174ea6",
        Generic.Subheading: "bold #174ea6",
        Generic.Emph: "#681da8",
        Generic.Strong: "bold #202124",
        Generic.Prompt: "bold #174ea6",
        Generic.Output: "#595d62",
        Error: "#a50e0e bg:#fad2cf",
    }
