# https://github.com/charmbracelet/vhs
Require zellij
Require nvim
Set Shell "bash"
Set FontFamily "GoogleSansCode Nerd Font Mono"
Set FontSize 17
Set Width 1500
Set Height 850
Set Padding 8
Set TypingSpeed 1ms
Set CursorBlink false
Source theme.tape
Hide
Type 'zellij --config config.kdl --new-session-with-layout layout.kdl --session fmind-screenshot'
Enter
Wait+Screen /UTF-8/
Sleep 2s
Show
Sleep 500ms
Type '/Result'
Enter
Sleep 500ms
Hide
Type '12ggVj'
Show
Sleep 500ms
Screenshot zellij.png
Escape
Hide
Type ':edit sample.md'
Enter
Wait+Screen /NORMAL.*sample.md/
Sleep 1s
Type ':redraw! | echo ""'
Enter
Type 'gg'
Show
Sleep 1s
Screenshot markdown.png
