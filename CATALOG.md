# Integration inventory

483 integration directories: 20 required by chezmoi and 463 additional developer integrations. Count one directory per integration, including lualine and the entire GTK/KDE bundle; do not count individual desktop components or terminal-inherited CLI colors as separate apps.

## Scope and acceptance

All 472 entries in [Dracula’s free catalog](https://draculatheme.com/) are represented in this inventory, reconciled on 2026-09-15. This measures directory coverage only. The 20 core paths remain protected by regression tests. Additional entries include experimental ports and incomplete drafts; native import, state behavior and visual acceptance are not established by this list.

[TODO.md](TODO.md) tracks native acceptance. [REVIEW.md](REVIEW.md) records concrete defects and [VALIDATION.md](VALIDATION.md) defines the evidence required. The GTK bundle includes an unfinished SDDM checkpoint. Avoid installing an additional port until its documented route matches your app version.

## Inventory

Core means a native theme consumed through chezmoi external files or copied configuration blocks. Additional integrations have offline checks; this does not establish native runtime acceptance. GTK includes an unfinished SDDM checkpoint, tracked in [TODO.md](TODO.md).

| Integration | Priority | Directory |
| --- | --- | --- |
| ABAP                     | Additional | [abap](abap/) |
| Ableton Live             | Additional | [ableton-live](ableton-live/) |
| Abricotine               | Additional | [abricotine](abricotine/) |
| AdiIRC                   | Additional | [adiirc](adiirc/) |
| Adminer                  | Additional | [adminer](adminer/) |
| Adobe                    | Additional | [adobe](adobe/) |
| Advent of Code           | Additional | [adventofcode](adventofcode/) |
| aerc                     | Additional | [aerc](aerc/) |
| Alacritty                | Additional | [alacritty](alacritty/) |
| Albert                   | Additional | [albert](albert/) |
| Alfred                   | Additional | [alfred](alfred/) |
| Aliucord                 | Additional | [aliucord](aliucord/) |
| AlphaI TUI               | Additional | [alphai-tui](alphai-tui/) |
| Amfora                   | Additional | [amfora](amfora/) |
| Anne Pro 2               | Additional | [anne-pro-2](anne-pro-2/) |
| Anytype                  | Additional | [anytype](anytype/) |
| Apache Superset          | Additional | [superset](superset/) |
| Apollo                   | Additional | [apollo](apollo/) |
| apt                      | Additional | [apt](apt/) |
| Archive of Our Own       | Additional | [archive-of-our-own](archive-of-our-own/) |
| Arduino IDE              | Additional | [arduino-ide](arduino-ide/) |
| Arduino Pro IDE          | Additional | [arduino-pro-ide](arduino-pro-ide/) |
| Aseprite                 | Additional | [aseprite](aseprite/) |
| Atom                     | Additional | [atom](atom/) |
| Atuin                    | Core       | [atuin](atuin/) |
| Audacity                 | Additional | [audacity](audacity/) |
| AutoAO3App               | Additional | [auto-ao3-app](auto-ao3-app/) |
| Bandcamp                 | Additional | [bandcamp](bandcamp/) |
| Base16                   | Additional | [base16](base16/) |
| Bashtop                  | Additional | [bashtop](bashtop/) |
| bat                      | Core       | [bat](bat/) |
| BBEdit                   | Additional | [bbedit](bbedit/) |
| Beamer                   | Additional | [beamer](beamer/) |
| Bear                     | Additional | [bear](bear/) |
| Beeper                   | Additional | [beeper](beeper/) |
| bemenu                   | Additional | [bemenu](bemenu/) |
| BetterCanvas             | Additional | [bettercanvas](bettercanvas/) |
| BetterDiscord            | Additional | [betterdiscord](betterdiscord/) |
| Beyond Compare 4         | Additional | [beyond-compare-4](beyond-compare-4/) |
| Blender                  | Additional | [blender](blender/) |
| Blink Shell              | Additional | [blink-shell](blink-shell/) |
| Blockbench               | Additional | [blockbench](blockbench/) |
| bobthefish               | Additional | [bobthefish](bobthefish/) |
| BookWyrm                 | Additional | [bookwyrm](bookwyrm/) |
| bottom                   | Core       | [bottom](bottom/) |
| Brackets                 | Additional | [brackets](brackets/) |
| bspwm                    | Additional | [bspwm](bspwm/) |
| BTCPay Server            | Additional | [btcpay-server](btcpay-server/) |
| btop                     | Additional | [btop](btop/) |
| CadZinho                 | Additional | [cadzinho](cadzinho/) |
| Calibre                  | Additional | [calibre](calibre/) |
| Campfire                 | Additional | [campfire](campfire/) |
| Caprine Messenger        | Additional | [caprine-messenger](caprine-messenger/) |
| Castero                  | Additional | [castero](castero/) |
| Cava                     | Additional | [cava](cava/) |
| ChatGPT                  | Additional | [chatgpt](chatgpt/) |
| Chatterino               | Additional | [chatterino](chatterino/) |
| Chrome                   | Additional | [chrome](chrome/) |
| Cider                    | Additional | [cider](cider/) |
| Claude Code              | Additional | [claude-code](claude-code/) |
| Cli-Visualizer           | Additional | [cli-visualizer](cli-visualizer/) |
| Clone Hero               | Additional | [clone-hero](clone-hero/) |
| Cmder                    | Additional | [cmder](cmder/) |
| Coda                     | Additional | [coda](coda/) |
| Code::Blocks             | Additional | [codeblocks](codeblocks/) |
| Codeforces               | Additional | [codeforces](codeforces/) |
| CodePen                  | Additional | [codepen](codepen/) |
| CodeRunner               | Additional | [coderunner](coderunner/) |
| colorls                  | Additional | [colorls](colorls/) |
| ColorSlurp               | Additional | [color-slurp](color-slurp/) |
| ConEmu                   | Additional | [conemu](conemu/) |
| CopyQ                    | Additional | [copyq](copyq/) |
| COSMIC Terminal          | Additional | [cosmic-terminal](cosmic-terminal/) |
| CotEditor                | Additional | [coteditor](coteditor/) |
| Couscous                 | Additional | [couscous](couscous/) |
| Cryptowatch              | Additional | [cryptowatch](cryptowatch/) |
| Cursor                   | Additional | [cursor](cursor/) |
| Cutter                   | Additional | [cutter](cutter/) |
| DankMaterialShell        | Additional | [dankmaterialshell](dankmaterialshell/) |
| Dash                     | Additional | [dash](dash/) |
| DeepSeek                 | Additional | [deepseek](deepseek/) |
| Delphi                   | Additional | [delphi](delphi/) |
| delta                    | Core       | [delta](delta/) |
| Dev-C++                  | Additional | [dev-cpp](dev-cpp/) |
| dircolors                | Additional | [dircolors](dircolors/) |
| Directory Opus           | Additional | [directory-opus](directory-opus/) |
| Dirtywave M8             | Additional | [m8](m8/) |
| Discord Bot Maker        | Additional | [discordbotmaker](discordbotmaker/) |
| Discourse                | Additional | [discourse](discourse/) |
| Ditto                    | Additional | [ditto](ditto/) |
| Django Admin             | Additional | [django-admin](django-admin/) |
| dmenu                    | Additional | [dmenu](dmenu/) |
| Docker                   | Additional | [docker](docker/) |
| DOOM Emacs               | Additional | [doom-emacs](doom-emacs/) |
| Dracula CSS              | Additional | [dracula-css](dracula-css/) |
| Drafts                   | Additional | [drafts](drafts/) |
| DuckDuckGo               | Additional | [duckduckgo](duckduckgo/) |
| Dunst                    | Additional | [dunst](dunst/) |
| Duolingo                 | Additional | [duolingo](duolingo/) |
| Dwarf Fortress           | Additional | [dwarf-fortress](dwarf-fortress/) |
| Dyalog APL               | Additional | [dyalog](dyalog/) |
| Eclipse                  | Additional | [eclipse](eclipse/) |
| EditPlus                 | Additional | [editplus](editplus/) |
| eM Client                | Additional | [em-client](em-client/) |
| Emacs                    | Additional | [emacs](emacs/) |
| EverythingToolbar        | Additional | [everythingtoolbar](everythingtoolbar/) |
| Evidence                 | Additional | [evidence](evidence/) |
| exa                      | Additional | [exa](exa/) |
| eza                      | Additional | [eza](eza/) |
| Facebook                 | Additional | [facebook](facebook/) |
| Facebook Messenger       | Additional | [facebook-messenger](facebook-messenger/) |
| Fastfetch                | Core       | [fastfetch](fastfetch/) |
| Fedilab                  | Additional | [fedilab](fedilab/) |
| Fig                      | Additional | [fig](fig/) |
| Figma                    | Additional | [figma](figma/) |
| Files                    | Additional | [files](files/) |
| Firefox                  | Additional | [firefox](firefox/) |
| Fish                     | Core       | [fish](fish/) |
| FL Studio 21             | Additional | [fl-studio-21](fl-studio-21/) |
| Flarum                   | Additional | [flarum](flarum/) |
| FlorisBoard              | Additional | [florisboard](florisboard/) |
| Flowlab                  | Additional | [flowlab](flowlab/) |
| Fluent Terminal          | Additional | [fluent-terminal](fluent-terminal/) |
| Fluxbox                  | Additional | [fluxbox](fluxbox/) |
| fman                     | Additional | [fman](fman/) |
| FocusWriter              | Additional | [focuswriter](focuswriter/) |
| FontForge                | Additional | [fontforge](fontforge/) |
| foot                     | Additional | [foot](foot/) |
| Forgejo                  | Additional | [forgejo](forgejo/) |
| ForkLift                 | Additional | [forklift](forklift/) |
| FreeCAD                  | Additional | [freecad](freecad/) |
| FreeTube                 | Additional | [freetube](freetube/) |
| FreshRSS                 | Additional | [freshrss](freshrss/) |
| Funkwhale                | Additional | [funkwhale](funkwhale/) |
| Fuzzel                   | Additional | [fuzzel](fuzzel/) |
| fzf                      | Core       | [fzf](fzf/) |
| Gajim                    | Additional | [gajim](gajim/) |
| GameMaker Studio         | Additional | [gamemaker-studio](gamemaker-studio/) |
| Gamepad Viewer           | Additional | [gamepad-viewer](gamepad-viewer/) |
| Geany                    | Additional | [geany](geany/) |
| Gedit                    | Additional | [gedit](gedit/) |
| Gemini                   | Additional | [gemini](gemini/) |
| ggplot2                  | Additional | [ggplot2](ggplot2/) |
| gh-dash                  | Core       | [gh-dash](gh-dash/) |
| Ghostty                  | Core       | [ghostty](ghostty/) |
| ghostwriter              | Additional | [ghostwriter](ghostwriter/) |
| GIMP                     | Additional | [gimp](gimp/) |
| Git                      | Additional | [git](git/) |
| GitHub                   | Additional | [github](github/) |
| GitHub Pages             | Additional | [gh-pages](gh-pages/) |
| Gitk                     | Additional | [gitk](gitk/) |
| GitKraken                | Additional | [gitkraken](gitkraken/) |
| GitLab                   | Additional | [gitlab](gitlab/) |
| Gitroll                  | Additional | [gitroll](gitroll/) |
| GMK                      | Additional | [gmk](gmk/) |
| GNOME Terminal           | Additional | [gnome-terminal](gnome-terminal/) |
| GNU grep                 | Additional | [grep](grep/) |
| GoAccess                 | Additional | [go-access](go-access/) |
| Godot                    | Additional | [godot](godot/) |
| Google Calendar          | Additional | [google-calendar](google-calendar/) |
| Google Search            | Additional | [google-search](google-search/) |
| GRUB                     | Additional | [grub](grub/) |
| GTK                      | Additional | [gtk](gtk/) |
| GtkSourceView            | Additional | [gtksourceview](gtksourceview/) |
| Hacker News              | Additional | [hacker-news](hacker-news/) |
| Harpy for Twitter        | Additional | [harpy-for-twitter](harpy-for-twitter/) |
| Helix                    | Additional | [helix](helix/) |
| Hermes Agent             | Additional | [hermes-agent](hermes-agent/) |
| Heroic Games Launcher    | Additional | [heroic-games-launcher](heroic-games-launcher/) |
| highlight.js             | Additional | [highlightjs](highlightjs/) |
| Home Assistant           | Additional | [home-assistant](home-assistant/) |
| Homepage                 | Additional | [homepage-app](homepage-app/) |
| Homer                    | Additional | [homer](homer/) |
| Hyper                    | Additional | [hyper](hyper/) |
| HyperX NGENUITY          | Additional | [ngenuity](ngenuity/) |
| Hyprland                 | Additional | [hyprland](hyprland/) |
| i3                       | Additional | [i3](i3/) |
| i3lock-color             | Additional | [i3lock-color](i3lock-color/) |
| IBM ACS                  | Additional | [acs](acs/) |
| IDA Pro                  | Additional | [ida](ida/) |
| IDLE                     | Additional | [idle](idle/) |
| ImageGlass               | Additional | [imageglass](imageglass/) |
| Infinity for Reddit      | Additional | [infinity-for-reddit](infinity-for-reddit/) |
| Inkscape                 | Additional | [inkscape](inkscape/) |
| Insomnia                 | Additional | [insomnia](insomnia/) |
| iSH                      | Additional | [ish](ish/) |
| iTerm2                   | Additional | [iterm2](iterm2/) |
| ITFY                     | Additional | [itfy](itfy/) |
| JabRef                   | Additional | [jabref](jabref/) |
| Javadoc                  | Additional | [javadoc](javadoc/) |
| JDownloader 2            | Additional | [jdownloader2](jdownloader2/) |
| Jellyfin                 | Additional | [jellyfin](jellyfin/) |
| JetBrains                | Additional | [jetbrains](jetbrains/) |
| jGRASP                   | Additional | [jgrasp](jgrasp/) |
| Joplin                   | Additional | [joplin](joplin/) |
| Jupyter Notebook         | Additional | [jupyter-notebook](jupyter-notebook/) |
| JupyterLab               | Additional | [jupyterlab](jupyterlab/) |
| k9s                      | Core       | [k9s](k9s/) |
| Kagi                     | Additional | [kagi](kagi/) |
| Kakoune                  | Additional | [kakoune](kakoune/) |
| Kali Browser             | Additional | [kali-browser](kali-browser/) |
| KanbanFlow               | Additional | [kanbanflow](kanbanflow/) |
| Kate                     | Additional | [kate](kate/) |
| KDiff3                   | Additional | [kdiff3](kdiff3/) |
| Keybr                    | Additional | [keybr](keybr/) |
| Keypirinha               | Additional | [keypirinha](keypirinha/) |
| KiCad                    | Additional | [kicad](kicad/) |
| Kitty                    | Additional | [kitty](kitty/) |
| Konsole                  | Additional | [konsole](konsole/) |
| Kristall                 | Additional | [kristall](kristall/) |
| Krita                    | Additional | [krita](krita/) |
| Kurozora                 | Additional | [kurozora](kurozora/) |
| LabPlot                  | Additional | [labplot](labplot/) |
| LaTeX                    | Additional | [latex](latex/) |
| Lazydocker               | Core       | [lazydocker](lazydocker/) |
| LazyGit                  | Core       | [lazygit](lazygit/) |
| LCD Smartie              | Additional | [lcd-smartie](lcd-smartie/) |
| LDoc                     | Additional | [ldoc](ldoc/) |
| LeetCode                 | Additional | [leetcode](leetcode/) |
| LeftWM                   | Additional | [leftwm](leftwm/) |
| Libreddit                | Additional | [libreddit](libreddit/) |
| LibreNMS                 | Additional | [librenms](librenms/) |
| LibreOffice              | Additional | [libreoffice](libreoffice/) |
| Lichess                  | Additional | [lichess](lichess/) |
| Light Table              | Additional | [light-table](light-table/) |
| LightPaper               | Additional | [lightpaper](lightpaper/) |
| LimeChat                 | Additional | [limechat](limechat/) |
| Linear                   | Additional | [linear](linear/) |
| Linux TTY                | Additional | [tty](tty/) |
| LiteIDE                  | Additional | [liteide](liteide/) |
| lnav                     | Additional | [lnav](lnav/) |
| Logseq                   | Additional | [logseq](logseq/) |
| lsd                      | Core       | [lsd](lsd/) |
| LTSpice                  | Additional | [ltspice](ltspice/) |
| lualine                  | Core       | [lualine](lualine/) |
| LXTerminal               | Additional | [lxterminal](lxterminal/) |
| MacDown                  | Additional | [macdown](macdown/) |
| MacDown CSS              | Additional | [macdown-css](macdown-css/) |
| macOS Color Picker       | Additional | [macos-color-picker](macos-color-picker/) |
| Mailspring               | Additional | [mailspring](mailspring/) |
| Makehuman                | Additional | [makehuman](makehuman/) |
| Mako                     | Additional | [mako](mako/) |
| man pages                | Additional | [man-pages](man-pages/) |
| Mantine                  | Additional | [mantine](mantine/) |
| Markdown CSS             | Additional | [markdown-css](markdown-css/) |
| Marp                     | Additional | [marp](marp/) |
| Marta                    | Additional | [marta](marta/) |
| MATLAB                   | Additional | [matlab](matlab/) |
| Matplotlib               | Additional | [matplotlib](matplotlib/) |
| Mattermost               | Additional | [mattermost](mattermost/) |
| MetaEditor               | Additional | [metaeditor](metaeditor/) |
| MetaTrader 5             | Additional | [metatrader5](metatrader5/) |
| Micro                    | Additional | [micro](micro/) |
| Microsoft Edge           | Additional | [microsoft-edge](microsoft-edge/) |
| Midnight Commander       | Additional | [midnight-commander](midnight-commander/) |
| MindNode                 | Additional | [mindnode](mindnode/) |
| Minecraft                | Additional | [minecraft](minecraft/) |
| Miniflux                 | Additional | [miniflux](miniflux/) |
| Mintty                   | Additional | [mintty](mintty/) |
| Misskey                  | Additional | [misskey](misskey/) |
| MiXplorer                | Additional | [mixplorer](mixplorer/) |
| MkDocs                   | Additional | [mkdocs](mkdocs/) |
| MobaXterm                | Additional | [mobaxterm](mobaxterm/) |
| Monkeytype               | Additional | [monkeytype](monkeytype/) |
| MonoDevelop              | Additional | [monodevelop](monodevelop/) |
| Mousepad                 | Additional | [mousepad](mousepad/) |
| mRemoteNG                | Additional | [mremoteng](mremoteng/) |
| MusicBee                 | Additional | [musicbee](musicbee/) |
| musikcube                | Additional | [musikcube](musikcube/) |
| Mutt                     | Additional | [mutt](mutt/) |
| MySQL Workbench          | Additional | [mysql-workbench](mysql-workbench/) |
| ncspot                   | Additional | [ncspot](ncspot/) |
| Neiki's Editor           | Additional | [neiki-editor](neiki-editor/) |
| Neiki's Page Editor      | Additional | [neiki-page-editor](neiki-page-editor/) |
| Neovim                   | Core       | [nvim](nvim/) |
| NetBeans                 | Additional | [netbeans](netbeans/) |
| New Tabs                 | Additional | [new-tabs](new-tabs/) |
| Newsboat                 | Additional | [newsboat](newsboat/) |
| NewTerm2                 | Additional | [newterm2](newterm2/) |
| Nextcloud                | Additional | [nextcloud](nextcloud/) |
| Nilesoft Shell           | Additional | [nilesoft-shell](nilesoft-shell/) |
| Nitter                   | Additional | [nitter](nitter/) |
| nnn                      | Additional | [nnn](nnn/) |
| Node Console             | Additional | [node-console](node-console/) |
| Noir                     | Additional | [noir](noir/) |
| Notepad++                | Additional | [notepad-plus-plus](notepad-plus-plus/) |
| Notesnook                | Additional | [notesnook](notesnook/) |
| Nova                     | Additional | [nova](nova/) |
| Nova Launcher            | Additional | [nova-launcher](nova-launcher/) |
| novelWriter              | Additional | [novel-writer](novel-writer/) |
| Nylas N1                 | Additional | [nylas-n1](nylas-n1/) |
| Nyxt                     | Additional | [nyxt](nyxt/) |
| Obsidian                 | Additional | [obsidian](obsidian/) |
| Oh My Posh               | Additional | [oh-my-posh](oh-my-posh/) |
| Omarchy                  | Additional | [omarchy](omarchy/) |
| omg.lol                  | Additional | [omglol](omglol/) |
| OneCommander             | Additional | [onecommander](onecommander/) |
| Openbox                  | Additional | [openbox](openbox/) |
| OpenCode                 | Core       | [opencode](opencode/) |
| OpenSCAD                 | Additional | [openscad](openscad/) |
| Oracle SQL Developer     | Additional | [oracle-sql-developer](oracle-sql-developer/) |
| Pandoc                   | Additional | [pandoc](pandoc/) |
| Pantheon Terminal        | Additional | [pantheon-terminal](pantheon-terminal/) |
| Papirus Folders          | Additional | [papirus-folders](papirus-folders/) |
| Passky                   | Additional | [passky](passky/) |
| Peacock Extension        | Additional | [peacock-extension](peacock-extension/) |
| PeerTube                 | Additional | [peertube](peertube/) |
| Pi Coding Agent          | Additional | [pi-coding-agent](pi-coding-agent/) |
| PL/SQL Developer         | Additional | [plsql-developer](plsql-developer/) |
| Plank                    | Additional | [plank](plank/) |
| Plymouth                 | Additional | [plymouth](plymouth/) |
| Polybar                  | Additional | [polybar](polybar/) |
| PolyMC                   | Additional | [polymc](polymc/) |
| Postbox                  | Additional | [postbox](postbox/) |
| Postman                  | Additional | [postman](postman/) |
| Powerlevel10k            | Additional | [powerlevel10k](powerlevel10k/) |
| Powerlevel10k for Oh My Posh | Additional | [p10k-oh-my-posh](p10k-oh-my-posh/) |
| PowerShell               | Additional | [powershell](powershell/) |
| PowerShell ISE           | Additional | [powershell-ise](powershell-ise/) |
| presenterm               | Additional | [presenterm](presenterm/) |
| Prism                    | Additional | [prism](prism/) |
| Prompt                   | Additional | [prompt](prompt/) |
| Protonmail               | Additional | [protonmail](protonmail/) |
| PsychoPy                 | Additional | [psychopy](psychopy/) |
| ptpython                 | Core       | [ptpython](ptpython/) |
| Pygments                 | Additional | [pygments](pygments/) |
| Pythonista               | Additional | [pythonista](pythonista/) |
| Pywal                    | Additional | [pywal](pywal/) |
| qBittorrent              | Additional | [qbittorrent](qbittorrent/) |
| Qt Creator               | Additional | [qtcreator](qtcreator/) |
| Qt5 / Qt6                | Additional | [qt5](qt5/) |
| QTerminal                | Additional | [qterminal](qterminal/) |
| Quassel                  | Additional | [quassel](quassel/) |
| Quiver                   | Additional | [quiver](quiver/) |
| Qutebrowser              | Additional | [qutebrowser](qutebrowser/) |
| R                        | Additional | [r](r/) |
| Rackula                  | Additional | [rackula](rackula/) |
| ranger                   | Additional | [ranger](ranger/) |
| Raycast                  | Additional | [raycast](raycast/) |
| Readwise Reader          | Additional | [readwise-reader](readwise-reader/) |
| ReNoise                  | Additional | [renoise](renoise/) |
| Replugged                | Additional | [replugged](replugged/) |
| Revolt                   | Additional | [revolt](revolt/) |
| Revolution IRC           | Additional | [revolution-irc](revolution-irc/) |
| Rime                     | Additional | [rime](rime/) |
| Rio                      | Additional | [rio](rio/) |
| Ripcord                  | Additional | [ripcord](ripcord/) |
| ripgrep                  | Additional | [ripgrep](ripgrep/) |
| Roam Research            | Additional | [roam-research](roam-research/) |
| Rofi                     | Additional | [rofi](rofi/) |
| RStudio                  | Additional | [rstudio](rstudio/) |
| RunJS                    | Additional | [runjs](runjs/) |
| Sandpack                 | Additional | [sandpack](sandpack/) |
| Scrivener                | Additional | [scrivener](scrivener/) |
| SecureCRT                | Additional | [securecrt](securecrt/) |
| Sequel Ace               | Additional | [sequel-ace](sequel-ace/) |
| Sequel Pro               | Additional | [sequel-pro](sequel-pro/) |
| SerenityOS               | Additional | [serenityos](serenityos/) |
| SideNotes                | Additional | [sidenotes](sidenotes/) |
| Signal Desktop           | Additional | [signal-desktop](signal-desktop/) |
| Sioyek                   | Additional | [sioyek](sioyek/) |
| Sketch                   | Additional | [sketch](sketch/) |
| Slack                    | Additional | [slack](slack/) |
| SmartGit                 | Additional | [smartgit](smartgit/) |
| Snappy Driver Installer  | Additional | [snappy-driver-installer](snappy-driver-installer/) |
| Snappy Driver Installer Origin | Additional | [snappy-driver-installer-origin](snappy-driver-installer-origin/) |
| Sniffnet                 | Additional | [sniffnet](sniffnet/) |
| SnippetsLab              | Additional | [snippetslab](snippetslab/) |
| SolidWorks               | Additional | [solidworks](solidworks/) |
| Spacemacs                | Additional | [spacemacs](spacemacs/) |
| SpeedCrunch              | Additional | [speedcrunch](speedcrunch/) |
| Spicetify                | Additional | [spicetify](spicetify/) |
| Spotify TUI              | Additional | [spotify-tui](spotify-tui/) |
| Spyder                   | Additional | [spyder](spyder/) |
| st                       | Additional | [st](st/) |
| Stack Overflow           | Additional | [stackoverflow](stackoverflow/) |
| Standard Notes           | Additional | [standard-notes](standard-notes/) |
| Starlight                | Additional | [astro-starlight](astro-starlight/) |
| Starship                 | Core       | [starship](starship/) |
| Starship Powerline Preset | Additional | [starship-powerline-preset](starship-powerline-preset/) |
| StationView              | Additional | [stationview](stationview/) |
| Steam                    | Additional | [steam](steam/) |
| Stirling PDF             | Additional | [stirling-pdf](stirling-pdf/) |
| Streamlit                | Additional | [streamlit](streamlit/) |
| Sublime Text             | Additional | [sublime-text](sublime-text/) |
| Subsonic                 | Additional | [subsonic](subsonic/) |
| Suckless Tabbed          | Additional | [suckless-tabbed](suckless-tabbed/) |
| Sumatra PDF              | Additional | [sumatra-pdf](sumatra-pdf/) |
| Swaylock                 | Additional | [swaylock](swaylock/) |
| SwayNotificationCenter   | Additional | [swaync](swaync/) |
| SwayOSD                  | Additional | [swayosd](swayosd/) |
| SwiftUI                  | Additional | [swiftui](swiftui/) |
| T3 Code                  | Additional | [t3code](t3code/) |
| TablePlus                | Additional | [tableplus](tableplus/) |
| Tabletop Simulator       | Additional | [tabletop-simulator](tabletop-simulator/) |
| Tailwind                 | Additional | [tailwind](tailwind/) |
| Taskwarrior              | Additional | [taskwarrior](taskwarrior/) |
| Telegram                 | Additional | [telegram](telegram/) |
| Telegram Android         | Additional | [telegram-android](telegram-android/) |
| Telegram iOS             | Additional | [telegram-ios](telegram-ios/) |
| Telegram macOS           | Additional | [telegram-macos](telegram-macos/) |
| Telegram X               | Additional | [telegram-x](telegram-x/) |
| Terminal.app             | Additional | [terminal-app](terminal-app/) |
| Terminator               | Additional | [terminator](terminator/) |
| Termite                  | Additional | [termite](termite/) |
| Termux                   | Additional | [termux](termux/) |
| TeXShop                  | Additional | [texshop](texshop/) |
| TeXstudio                | Additional | [texstudio](texstudio/) |
| Textastic                | Additional | [textastic](textastic/) |
| TextMate                 | Additional | [textmate](textmate/) |
| Textual                  | Additional | [textual](textual/) |
| TeXworks                 | Additional | [texworks](texworks/) |
| The Lounge               | Additional | [thelounge](thelounge/) |
| Thonny                   | Additional | [thonny](thonny/) |
| ThumbKey                 | Additional | [thumb-key](thumb-key/) |
| Thunderbird              | Additional | [thunderbird](thunderbird/) |
| TiddlyWiki               | Additional | [tiddlywiki](tiddlywiki/) |
| tig                      | Additional | [tig](tig/) |
| Tilix                    | Additional | [tilix](tilix/) |
| tint2                    | Additional | [tint2](tint2/) |
| tlrc                     | Additional | [tlrc](tlrc/) |
| tmux                     | Additional | [tmux](tmux/) |
| Todoist                  | Additional | [todoist](todoist/) |
| tofi                     | Additional | [tofi](tofi/) |
| Total Commander          | Additional | [total-commander](total-commander/) |
| Tower                    | Additional | [tower](tower/) |
| Tridactyl                | Additional | [tridactyl](tridactyl/) |
| Trudido                  | Additional | [trudido](trudido/) |
| Tumblr                   | Additional | [tumblr](tumblr/) |
| Tut                      | Additional | [tut](tut/) |
| tym                      | Additional | [tym](tym/) |
| Typora                   | Additional | [typora](typora/) |
| Ueli                     | Additional | [ueli](ueli/) |
| Ulauncher                | Additional | [ulauncher](ulauncher/) |
| Ulysses                  | Additional | [ulysses](ulysses/) |
| Unigram                  | Additional | [unigram](unigram/) |
| Unraid                   | Additional | [unraid](unraid/) |
| Unreal Engine            | Additional | [unreal-engine](unreal-engine/) |
| Uptime Kuma              | Additional | [uptime-kuma](uptime-kuma/) |
| Vesktop Discord          | Additional | [vesktop-discord](vesktop-discord/) |
| Vim                      | Additional | [vim](vim/) |
| Vimium                   | Additional | [vimium](vimium/) |
| vis                      | Additional | [vis](vis/) |
| Visual Basic 6           | Additional | [visual-basic-6](visual-basic-6/) |
| Visual Spigot            | Additional | [visual-spigot](visual-spigot/) |
| Visual Studio            | Additional | [visual-studio](visual-studio/) |
| Vital                    | Additional | [vital](vital/) |
| Vivado                   | Additional | [vivado](vivado/) |
| Vivaldi                  | Additional | [vivaldi](vivaldi/) |
| Vortex Mod Manager       | Additional | [vortex-mod-manager](vortex-mod-manager/) |
| VS Code                  | Additional | [vscode](vscode/) |
| Wallpaper                | Additional | [wallpaper](wallpaper/) |
| Warp                     | Additional | [warp](warp/) |
| Waybar                   | Additional | [waybar](waybar/) |
| WezTerm                  | Additional | [wezterm](wezterm/) |
| WhatsApp Web             | Additional | [whatsapp-web](whatsapp-web/) |
| Windows Terminal         | Additional | [windows-terminal](windows-terminal/) |
| WindTerm                 | Additional | [windterm](windterm/) |
| Wing                     | Additional | [wing](wing/) |
| Wiremix                  | Additional | [wiremix](wiremix/) |
| WOB                      | Additional | [wob](wob/) |
| Wofi                     | Additional | [wofi](wofi/) |
| Wolfram Notebooks        | Additional | [wolfram-notebooks](wolfram-notebooks/) |
| WordPress                | Additional | [wordpress](wordpress/) |
| Wox                      | Additional | [wox](wox/) |
| WP                       | Additional | [wp](wp/) |
| x64dbg                   | Additional | [x64dbg](x64dbg/) |
| XChat / HexChat          | Additional | [xchat](xchat/) |
| Xcode                    | Additional | [xcode](xcode/) |
| xdbg                     | Additional | [xdbg](xdbg/) |
| Xfce4 Terminal           | Additional | [xfce4-terminal](xfce4-terminal/) |
| Xournal++                | Additional | [xournalpp](xournalpp/) |
| Xresources               | Additional | [xresources](xresources/) |
| Yakuake                  | Additional | [yakuake](yakuake/) |
| Yazi                     | Core       | [yazi](yazi/) |
| YouTube                  | Additional | [youtube](youtube/) |
| YouTube Music Desktop    | Additional | [youtube-music-desktop](youtube-music-desktop/) |
| YunoHost                 | Additional | [yunohost](yunohost/) |
| Zathura                  | Additional | [zathura](zathura/) |
| Zed                      | Additional | [zed](zed/) |
| Zellij                   | Core       | [zellij](zellij/) |
| Zsh                      | Additional | [zsh](zsh/) |
| zsh-syntax-highlighting  | Additional | [zsh-syntax-highlighting](zsh-syntax-highlighting/) |
