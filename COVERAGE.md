# App coverage

Fmind provides 99 native integrations. The [free Dracula catalog](https://draculatheme.com/) listed 472 themes when reviewed on 2026-09-14. Its entries include applications, plugins, website styles, platforms, wallpapers and hardware; that count is not directly comparable to app folders. No Dracula Pro assets were used.

The [README](README.md) lists every shipped file and its installation instructions. Ports use Fmind’s light palette, with dark text, pale highlighted surfaces and bright accents. Dracula is the coverage reference. Notepad++ lexer definitions and Qt Creator editor definitions are adapted from MIT-licensed free Dracula ports, with their notices retained alongside the files; all ports use Fmind’s palette. WindTerm’s UI layout, icon selectors and native scope definitions are adapted from its MIT-licensed free Dracula port, with its notice retained in `windterm/LICENSE`.

The [472-entry catalog checklist](CATALOG.md) tracks the full requested scope, with shipped ports and explicit pending entries. This is the completion baseline; the areas below summarize it.

## Scope of the current ports

| Area | Coverage |
| --- | --- |
| Code editors | Vim, Neovim, Emacs, VS Code, Helix, Zed, Micro, Sublime Text, JetBrains, Kate, Gedit, Geany, Xcode, Notepad++, Qt Creator, TextMate, NetBeans, Eclipse, Code::Blocks, Dev-C++, Atom, Brackets and lualine. JetBrains and Sublime are editor color schemes, not complete application UI themes. |
| Notes and browsers | Obsidian and Typora; Chrome and Firefox interface themes. Browser themes do not restyle web pages. Firefox’s local temporary install ends at restart; permanent installation requires signing. |
| Terminals | Alacritty, Ghostty, Kitty, WezTerm, foot, Rio, Konsole, iTerm2, Windows Terminal, GNOME Terminal, Hyper, Terminator, Xfce4 Terminal, Mintty, Termux, Xresources, Terminal.app, Tilix, Warp, MobaXterm, ConEmu, QTerminal, LXTerminal, Termite, st, Fluent Terminal, WindTerm, COSMIC Terminal, Pantheon Terminal and tym. |
| Shells and terminal tools | Fish, PowerShell input highlighting, zsh-syntax-highlighting, Starship, tmux, Zellij, bat, delta, fzf, Atuin, bottom, btop, Fastfetch, gh-dash, k9s, Lazydocker, LazyGit, lsd, OpenCode, ptpython and Yazi. |
| Linux desktop | i3, bspwm and Hyprland window colors; Waybar, Polybar, Rofi, Wofi, Fuzzel, Dunst, SwayNotificationCenter, SwayOSD, WOB and Zathura; Swaylock and Hyprlock visual settings. Several are fragments for existing configurations. |
| Python tools | Streamlit application colors, Matplotlib plot styles, IDLE highlighting, a Pygments style, Spyder syntax settings and RStudio. |

KSyntaxHighlighting apps can use the Kate scheme, GtkSourceView apps can use the Gedit scheme, and Xresource-aware terminals can use Xresources. VS Code derivatives may accept the local extension, but they are not counted as separately tested integrations.

## Remaining work

Full Dracula parity is not claimed. These areas remain required work toward full catalog parity. The checklist also includes every remaining catalog entry:

| Area | Examples still missing | Work needed |
| --- | --- | --- |
| Other major IDEs | Visual Studio, Arduino IDE and Arduino Pro IDE | Native platform validation and language-specific coverage. |
| More terminals | NewTerm2, SecureCRT and mRemoteNG | Native profile formats and import validation. |
| Python and data IDEs | JupyterLab, Jupyter Notebook, Thonny, MATLAB | Application-specific extensions or settings and runtime checks. |
| Full desktop themes | GTK, Qt and KDE | Widget-state coverage and broader desktop testing. The current fragments do not substitute for these. |
| Productivity and communication | Slack, Telegram, Raycast, Alfred, Logseq, Thunderbird | App-specific import formats, supported customization boundaries and ongoing UI maintenance. |
| Creative and specialist tools | Blender, Godot, GIMP, Inkscape, KiCad | Domain-specific colors and representative native fixtures. |
| Websites and legacy integrations | Site-specific browser styles, discontinued editors | Native customization routes, selector coverage and legacy format validation. |

## Validation boundary

The repository gate checks native document parsing, palette use, terminal slot parity, selected text, filled controls and syntax contrast. Available local runtimes provide additional checks, including Vim/Neovim highlighting. The two synthetic screenshots exercise the existing terminal demonstration; they are not screenshots of every supported application.

The new ports have not all been launched in their target applications. Runtime changes, third-party plugins, transparency, user overrides and arbitrary ANSI background combinations remain outside the contrast claim. Setup and checks do not install themes into user profiles or call live application services.

The Terminal.app port has decoded NSColor archive checks, and Xcode has RGBA and font-field checks. IDLE is loaded through its installed Python parser, and Pygments renders real Python and diff samples. The new Windows/macOS desktop ports have no target-platform runtime proof yet. ConEmu uses BGR-encoded Windows slot ordering and reserves slot 15 as the white canvas; that one slot is not a readable foreground on white. Other terminal ANSI slots retain Fmind’s contrast contract.

Notepad++ includes 60 lexers and 842 syntax styles, with unique per-lexer IDs and a corrected Verilog line-comment collision from the reference port. Qt Creator defines all 441 color roles in the 20.0.1 native theme enum, plus 66 editor styles, with no external theme includes. Spyder targets the released 6.1 configuration format. RStudio CSS uses Ace and documented theme selectors, with the light Modern UI as its base. These ports have offline structural and contrast checks; target-app rendering and import validation remain outstanding.

Hyprland targets the current Lua configuration (0.55+, checked against the 0.56.2 example); its Hyprlock companion contains only visual widgets. Swaylock uses core color options without an effects fork. Fuzzel covers all twelve documented RGBA color roles, and dmenu includes all three native color schemes. SwayNotificationCenter targets 0.12.6 and imports the app’s installed layout, with Fmind native CSS variables and overrides for built-in notifications and widgets. Wofi parses without diagnostics in GTK 3.24.38, and SwayOSD in GTK 4.8.3. SwayNotificationCenter requires GTK 4.16.13 or newer, which is unavailable here; its full stylesheet has CSS syntax and contrast checks but no matching native-parser proof. The dmenu header compiles as C99 with warnings treated as errors against its native scheme enum. Live compositor, launcher, notification, lock-screen and panel rendering remain unverified.

The terminal batch includes all sixteen ANSI slots for nine ports; QTerminal and COSMIC also define dim colors. WindTerm includes 55 native styles and 50 syntax scope rules, plus its Qt UI stylesheet and icon color selectors. Pantheon’s custom palette and appearance keys are checked against the native settings schema. st reserves separate default background and cursor slots so ANSI white remains readable on the white canvas. The native extended 256-color palette and arbitrary applications’ background choices are outside the ANSI contrast contract. Target-app rendering and imports still require separate verification.

Additional offline evidence for this batch: COSMIC’s RON file deserializes with its native `ColorScheme` and `ColorSchemeAnsi` definitions and RON 0.11; Qt QSettings loads QTerminal’s color groups; GLib parses the VTE ports’ key files and Pantheon’s seven typed settings; and st’s header compiles warning-free as C99 and returns the intended default color indices. WindTerm’s QSS parses with Qt using asset loading disabled, and all 27 original asset paths are separately verified against its 2.7.0 release archive. This does not establish rendering in WindTerm’s custom widgets or its bundled Qt version.

The IDE batch adds NetBeans’ 27 MIME profiles and shared settings (549 color entries), Code::Blocks 25.03 coverage for all 62 native lexers (1,324 named style entries), Dev-C++ C/C++ syntax and editor state pairs, Atom’s syntax-theme package and public syntax variables, and a light Brackets CodeMirror theme. Eclipse includes 47 theme roles plus 382 native preference entries for core editors, JDT, CDT, Ant, the debug console and PyDev. NetBeans, Atom and Eclipse role definitions retain the free reference ports’ MIT notices. The NetBeans import excludes unrelated reference settings and obsolete user metadata.

All 30 NetBeans color documents also validate offline against its native Fonts and Colors 1.1 DTD. Code::Blocks’ stored style-name sets match all 62 lexers in the official 25.03 source archive, and Atom’s stylesheet compiles with Less 4.9.1. These checks do not run the target IDEs or Atom’s embedded Less version.

These are native editor/theme packages with structural, language-role and contrast checks. Light application appearance remains a separate setting where the application separates UI and syntax themes. Full target-IDE rendering, plugin interactions and native imports remain unverified; a passing format check does not establish those outcomes. Visual Studio and both Arduino catalog entries remain pending.
