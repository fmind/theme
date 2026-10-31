# Fmind light theme for Kakoune
# Sets every face in Kakoune's colors/default.kak and built-in face registry:
# `colorscheme` only sources this file, so unset faces would keep ANSI defaults.

evaluate-commands %sh{
    ground="rgb:ffffff"
    text="rgb:202124"
    muted="rgb:595d62"
    border="rgb:9aa0a6"
    surface="rgb:f1f3f4"
    selection="rgb:d2e3fc"
    focus="rgb:4285f4"
    blue="rgb:174ea6"
    green="rgb:0d652d"
    success="rgb:34a853"
    red="rgb:a50e0e"
    error="rgb:ea4335"
    orange="rgb:934900"
    warning="rgb:e37400"
    yellow="rgb:fbbc04"
    purple="rgb:681da8"
    teal="rgb:00636d"

    echo "
        face global value ${orange}
        face global type ${purple}
        face global variable ${text}
        face global module ${blue}
        face global function ${blue}
        face global string ${green}
        face global keyword ${blue}+b
        face global operator ${text}
        face global attribute ${purple}
        face global comment ${muted}
        face global documentation comment
        face global meta ${purple}
        face global builtin ${purple}

        face global title ${blue}+b
        face global header ${blue}
        face global mono ${blue}
        face global block ${purple}
        face global link ${blue}+u
        face global bullet ${blue}
        face global list ${blue}

        face global Default ${text},${ground}
        face global PrimarySelection ${text},${selection}
        face global SecondarySelection ${muted},${surface}
        face global PrimaryCursor ${text},${focus}+fg
        face global SecondaryCursor ${ground},${muted}+fg
        face global PrimaryCursorEol ${ground},${teal}+fg
        face global SecondaryCursorEol ${ground},${muted}+fg
        face global LineNumbers ${muted},${surface}
        face global LineNumberCursor ${blue},${surface}+b
        face global LineNumbersWrapped ${muted},${surface}
        face global LineHighlight ${text},${surface}
        face global WrapMarker ${border},${ground}
        face global MenuForeground ${text},${selection}+b
        face global MenuBackground ${text},${surface}
        face global MenuInfo ${muted}
        face global Information ${text},${surface}
        face global InlineInformation Information
        face global Error ${ground},${red}
        face global DiagnosticError default,default,${error}+c
        face global DiagnosticWarning default,default,${warning}+c
        face global StatusLine ${text},${surface}
        face global StatusLineMode ${text},${success}+b
        face global StatusLineInfo ${blue},${surface}
        face global StatusLineValue ${green},${surface}
        face global StatusCursor ${ground},${blue}
        face global Prompt ${blue},${surface}
        face global MatchingChar ${text},${yellow}+b
        face global Whitespace ${border}+f
        face global WhitespaceIndent Whitespace
        face global BufferPadding ${border},${ground}
    "
}
