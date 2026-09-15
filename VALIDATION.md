# Readability and runtime validation

Use the complete palette across the theme family; individual apps should use only colors with meaningful roles. Dark colors carry text, pale colors carry selected/diff surfaces, and bright colors carry accents with contrasting labels. Gray `#9AA0A6` is decorative; essential control boundaries and scrollbar thumbs use dark gray. Text must reach 4.5:1; essential non-text indicators must reach 3:1 against adjacent surfaces.

## Shared state roles

These are defaults for new and restored ports, adapted to native app affordances. The refinement applies them to Neovim search and Zellij ribbons first; existing ports need individual review before claiming family-wide alignment. Individual apps use only colors with meaningful roles.

| State                       | Foreground                                  | Background or accent                                       | Additional cue                                                |
| --------------------------- | ------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------- |
| Ordinary content            | Charcoal `#202124`                          | White `#FFFFFF`                                            | Native text hierarchy                                         |
| Inactive chrome             | Charcoal `#202124`                          | Panel `#F1F3F4`; pale blue `#D2E3FC` for ribbon separation | Keep native tile boundaries                                   |
| Hover                       | Charcoal `#202124`                          | Panel `#F1F3F4`                                            | Preserve control outline on white surfaces                    |
| Keyboard focus              | Charcoal `#202124`                          | Dark blue `#174EA6` outline                                | Visible native focus ring                                     |
| Selection / completion      | Charcoal `#202124`                          | Pale blue `#D2E3FC`                                        | Native selection or active-row indicator                      |
| Active ribbon / mode        | Charcoal `#202124`                          | Yellow `#FBBC04`                                           | Active label and native emphasis                              |
| Ordinary search match       | Charcoal `#202124`                          | Pale yellow `#FEEFC3`                                      | Native occurrence markers                                     |
| Current / incremental match | Charcoal `#202124`, bold                    | Yellow `#FBBC04`                                           | Bold plus native match count/navigation                       |
| Disabled / secondary text   | Dark gray `#595D62`                         | White or panel                                             | Native disabled semantics; avoid opacity that lowers contrast |
| Added / removed / changed   | Dark semantic foreground or readable syntax | Pale green / red / yellow                                  | Signs, labels or changed-word emphasis                        |

Bright blue remains a cursor and deliberate active accent. Orange remains a warning accent. Do not make every inactive control saturated, or use all palette colors merely to fill a checklist. Test foreground/background pairs after native compositing and selection overrides.

## Repeatable checks

| Command                           | What it proves                                                                                                                                                                    | Boundary                                                                                                    |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `mise run check`                  | Native documents, palette consistency, contrast, actual bat gutter/token output, and native Neovim completion, diagnostic floats, changed-word diffs, search and visual selection | Does not render every app or every plugin state                                                             |
| `mise run check:terminal-runtime` | Ghostty's native loader accepts the theme and enables `minimum-contrast = 4.5`                                                                                                    | Requires Ghostty; configuration acceptance is not rendered-pixel proof                                      |
| `mise run check:gtk-runtime`      | GTK 3 computed colors for normal, hover, focused and disabled controls; selected text and toggle state changes                                                                    | Requires GTK 3 Broadway and a Python interpreter with PyGObject; no complete desktop session or GTK 4 proof |
| `mise run screenshots`            | Two synthetic Neovim/Fish/Zellij captures, including search, selection, Markdown and a numbered bat preview                                                                       | Requires the capture dependencies listed in README; captures use VHS, not Ghostty's renderer                |

The GTK check launches a private Broadway display with isolated HOME/XDG paths, a Unix socket, in-memory settings and fatal GTK warnings. It loads the checkout's stylesheet directly and never installs a theme. Set `BROADWAYD` if the daemon is outside PATH and `GTK_PYTHON` if PyGObject is provided by an interpreter other than `/usr/bin/python3`. Dependencies must be installed before running the check; the check itself never downloads packages. Its temporary display, configuration and processes are cleaned up on exit.

## Core 20 validation matrix

These are the protected workstation paths and the evidence actually provided by this repository. Static checks do not imply native schema validation or a running TUI. The previous matrix included obsolete hex values, incorrect ratios and nonexistent test references; the authoritative color values remain in the native files and `checks/palette.yaml`.

| Integration | Native file | Repository evidence | Remaining boundary |
| --- | --- | --- | --- |
| Atuin | `atuin/fmind.toml` | TOML parse and palette scan | Native search UI unverified |
| bat | `bat/fmind.tmTheme` | Plist roles, native SGR output and syntax fixtures | Parser-specific syntax limits below |
| bottom | `bottom/fmind.toml` | TOML parse and palette scan | Native graphs and table states unverified |
| delta | `delta/fmind.gitconfig` | Git configuration parser and palette scan | Native diff rendering unverified in this review |
| Fastfetch | `fastfetch/fmind.json` | JSON parse and palette scan | Native output unverified |
| Fish | `fish/fmind.fish` | Native syntax parser and synthetic shell screenshot | Every interactive completion state unverified |
| fzf | `fzf/fmind.conf` | Palette scan and actual scrollbar/background contrast | Native fuzzy-finder state matrix unverified |
| gh-dash | `gh-dash/fmind.yml` | YAML parse and palette scan | GitHub-connected TUI not exercised |
| Ghostty | `ghostty/fmind` | Slot parity, foreground contrast and isolated native loader | Arbitrary application output depends on the contrast safeguard |
| k9s | `k9s/fmind.yaml` | YAML parse and palette scan | No Kubernetes session exercised |
| Lazydocker | `lazydocker/fmind.yml` | YAML parse and palette scan | No Docker session exercised |
| LazyGit | `lazygit/fmind.yml` | YAML parse and palette scan | Native interaction states unverified |
| lsd | `lsd/fmind.yaml` | YAML parse; named colors inherit the terminal palette | Native listing unverified |
| lualine | `lualine/fmind.lua` | Direct Lua theme and palette scan | Plugin-specific mode rendering unverified in this review |
| Neovim | `nvim/colors/fmind.lua` | Native headless Lua assertions, syntax highlighting, search, selection and screenshots | Third-party plugins and arbitrary languages outside fixtures |
| OpenCode | `opencode/fmind.json` | JSON definitions, references, syntax roles and diff pair contrast | Native coding-agent UI unverified |
| ptpython | `ptpython/fmind.py` | Executes style configuration using prompt-toolkit; checks style colors | Interactive REPL states unverified |
| Starship | `starship/fmind.toml` | TOML parse and palette scan | Native prompt combinations unverified |
| Yazi | `yazi/fmind.toml` | TOML parse and filled-label contrast | Native file-manager interaction unverified |
| Zellij | `zellij/fmind.kdl` | Tile color/contrast assertions and synthetic native screenshots | Every layout, plugin and interaction outside the fixtures |

## ANSI compatibility

The default ANSI palette prioritizes readable foreground text on the white canvas. Keep the existing dark slots, including slots named white, and duplicate normal/bright colors; brightness is not a reliable semantic distinction in this theme. Use bold, labels or explicit app colors when distinction matters. This policy does not promise arbitrary ANSI foreground/background compatibility.

Dark ANSI foregrounds remain readable on white, but applications may also use those same slots as backgrounds. Ghostty's `minimum-contrast = 4.5` adjusts otherwise unreadable foreground/background combinations; adjusted colors may fall outside the palette. Other terminals need their own equivalent safeguard or explicit application styles. The 256-color cube and grayscale ramp are not remapped. Test background-dependent apps with the actual target terminal; configure explicit contrasting app styles or a verified renderer safeguard where necessary. Leave unsupported combinations documented as gaps. Never treat Ghostty configuration acceptance or VHS captures as proof that another terminal corrects these combinations.

For visual acceptance in the configured Ghostty terminal, run:

```sh
python checks/samples/ansi.py
```

Inspect the white-on-black and white-on-red examples and all 256 matrix cells. Repeat after changing the terminal renderer, transparency, or contrast policy. This is a manual check, not a claim that the offline gate measured rendered pixels.

## Port acceptance

Track format validation, native import/loading, state behavior, and visual inspection separately when extending the app catalog. Prioritize the apps actually used on the workstation. Exercise ordinary and disabled controls, focus/hover, selected text, completion menus, search results, diagnostic messages and diffs where the app supports them. Distinguish semantic states with labels, glyphs, borders or emphasis as well as color. A supplied theme file alone does not establish runtime acceptance.

The two retained screenshots remain synthetic terminal demonstrations. Full GUI sessions, third-party plugins, application-specific painting and current Windows/macOS runtimes require separate evidence.

## Release review — 2026-09-15

The isolated review candidate passes all 377 offline tests, Ruff checks and formatting, fish parsing, Git configuration parsing, actionlint, the pedantic offline zizmor audit, and the README site build. The candidate excludes concurrently created, untracked wallpaper artwork. No assertions were weakened to bypass that unrelated directory; the same gate passed in the isolated candidate.

The live Dracula catalog still has the same 472 entry slugs as the baseline; the new offline mapping test covers each slug, including ten directory aliases. This proves inventory coverage only. Adobe’s new ASE palette is decoded block by block against all 20 named source colors. Anytype uses native custom CSS properties with actual text/surface contrast checks. Neither Adobe nor Anytype was opened in a native app session.

Ghostty’s isolated native loader accepts the theme and enables `minimum-contrast = 4.5`. Both synthetic terminal screenshots were refreshed successfully with VHS, using the shared installed tools. The README page passed Chromium checks at 1440px and 390px: all three images loaded, the installation table was reachable, no JavaScript exceptions occurred, and the page had no horizontal overflow. These browser checks do not certify every third-party theme.

The optional GTK runtime check is blocked by a missing GTK 3 `broadwayd` executable; PyGObject and a suitable GTK Python interpreter are also prerequisites. The exact failure was `Install GTK 3 broadwayd or set BROADWAYD to its binary; GTK_PYTHON must provide PyGObject`. No full GTK/KDE or SDDM native campaign was rerun.

The workstation’s global mise configuration failed on an unrelated `pipx:google-colab-cli` lock option. Project setup succeeds with `MISE_IGNORED_CONFIG_PATHS` pointing to that global config; no workstation configuration was changed. The disposable clone used a copied syntax cache and its own Python environment. Its first dependency sync fell back from hardlinks to copies across filesystems; subsequent checks passed without warnings.

Native acceptance remains open in [TODO.md](TODO.md). Known incomplete Minecraft and Aseprite drafts are not working ports. Release notes must retain these limits; a version tag does not turn inventory coverage into functional parity.
