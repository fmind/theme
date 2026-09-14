# App coverage

Fmind provides 69 native integrations. The [free Dracula catalog](https://draculatheme.com/) listed 472 themes when reviewed on 2026-09-14. Its entries include applications, plugins, website styles, platforms, wallpapers and hardware; that count is not directly comparable to app folders. No Dracula Pro assets were used.

The [README](README.md) lists every shipped file and its installation instructions. Ports use Fmind’s light palette, with dark text, pale highlighted surfaces and bright accents. These are independently authored ports; Dracula is the coverage reference.

The [472-entry catalog checklist](CATALOG.md) tracks the full requested scope, with shipped ports and explicit pending entries. This is the completion baseline; the areas below summarize it.

## Scope of the current ports

| Area | Coverage |
| --- | --- |
| Code editors | Vim, Neovim, Emacs, VS Code, Helix, Zed, Micro, Sublime Text, JetBrains, Kate, Gedit, Geany, Xcode and lualine. JetBrains and Sublime are editor color schemes, not complete application UI themes. |
| Notes and browsers | Obsidian and Typora; Chrome and Firefox interface themes. Browser themes do not restyle web pages. Firefox’s local temporary install ends at restart; permanent installation requires signing. |
| Terminals | Alacritty, Ghostty, Kitty, WezTerm, foot, Rio, Konsole, iTerm2, Windows Terminal, GNOME Terminal, Hyper, Terminator, Xfce4 Terminal, Mintty, Termux, Xresources, Terminal.app, Tilix, Warp, MobaXterm and ConEmu. |
| Shells and terminal tools | Fish, PowerShell input highlighting, zsh-syntax-highlighting, Starship, tmux, Zellij, bat, delta, fzf, Atuin, bottom, btop, Fastfetch, gh-dash, k9s, Lazydocker, LazyGit, lsd, OpenCode, ptpython and Yazi. |
| Linux desktop | i3 window colors, Waybar, Rofi, Dunst and Zathura. These are color fragments for existing configurations. |
| Python tools | Streamlit application colors, Matplotlib plot styles, IDLE highlighting and a Pygments style. |

KSyntaxHighlighting apps can use the Kate scheme, GtkSourceView apps can use the Gedit scheme, and Xresource-aware terminals can use Xresources. VS Code derivatives may accept the local extension, but they are not counted as separately tested integrations.

## Remaining work

Full Dracula parity is not claimed. These areas remain required work toward full catalog parity. The checklist also includes every remaining catalog entry:

| Area | Examples still missing | Work needed |
| --- | --- | --- |
| Other major IDEs | Notepad++, Visual Studio, NetBeans, Eclipse, Qt Creator | Native platform validation and language-specific coverage. |
| More terminals | Tabby, Qterminal, WindTerm, Termite, LXTerminal | Native profile formats and import validation. |
| Python and data IDEs | JupyterLab, Jupyter Notebook, Spyder, RStudio | Application-specific extensions or settings and runtime checks. |
| Full desktop themes | GTK, Qt, KDE, Hyprland | Widget-state coverage and broader desktop testing. The current fragments do not substitute for these. |
| Productivity and communication | Slack, Telegram, Raycast, Alfred, Logseq, Thunderbird | App-specific import formats, supported customization boundaries and ongoing UI maintenance. |
| Creative and specialist tools | Blender, Godot, GIMP, Inkscape, KiCad | Domain-specific colors and representative native fixtures. |
| Websites and legacy integrations | Site-specific browser styles, discontinued editors | Native customization routes, selector coverage and legacy format validation. |

## Validation boundary

The repository gate checks native document parsing, palette use, terminal slot parity, selected text, filled controls and syntax contrast. Available local runtimes provide additional checks, including Vim/Neovim highlighting. The two synthetic screenshots exercise the existing terminal demonstration; they are not screenshots of every supported application.

The new ports have not all been launched in their target applications. Runtime changes, third-party plugins, transparency, user overrides and arbitrary ANSI background combinations remain outside the contrast claim. Setup and checks do not install themes into user profiles or call live application services.

The Terminal.app port has decoded NSColor archive checks, and Xcode has RGBA and font-field checks. IDLE is loaded through its installed Python parser, and Pygments renders real Python and diff samples. The new Windows/macOS desktop ports have no target-platform runtime proof yet. ConEmu uses BGR-encoded Windows slot ordering and reserves slot 15 as the white canvas; that one slot is not a readable foreground on white. Other terminal ANSI slots retain Fmind’s contrast contract.
