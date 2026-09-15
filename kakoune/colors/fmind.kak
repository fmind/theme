# Fmind light theme for Kakoune

evaluate-commands %sh{
    ground="rgb:ffffff"
    text="rgb:202124"
    muted="rgb:595d62"
    surface="rgb:f1f3f4"
    selection="rgb:d2e3fc"
    blue="rgb:174ea6"
    green="rgb:0d652d"
    red="rgb:a50e0e"
    orange="rgb:934900"
    purple="rgb:681da8"
    teal="rgb:00636d"

    echo "
        face global value ${blue}
        face global type ${blue}
        face global variable ${text}
        face global module ${blue}
        face global function ${blue}
        face global string ${green}
        face global keyword ${blue}+b
        face global operator ${blue}
        face global attribute ${orange}
        face global comment ${muted}+i
        face global title ${blue}+b
        face global header ${blue}
        face global Default ${text},${ground}
        face global PrimarySelection ${text},${selection}
        face global SecondarySelection ${muted},${surface}
        face global LineNumbers ${muted},${surface}
        face global LineHighlight ${text},${surface}
    "
}
