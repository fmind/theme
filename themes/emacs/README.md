# Fmind for Emacs

Files: [fmind-theme.el](fmind-theme.el).

Format: [Emacs Lisp manual: Custom Themes](https://www.gnu.org/software/emacs/manual/html_node/elisp/Custom-Themes.html)

## Installation

Copy to `~/.emacs.d/themes/`, add that directory to `custom-theme-load-path`, then use `M-x load-theme` → `fmind`.

## Spacemacs

[Spacemacs](https://www.spacemacs.org/) loads this Emacs theme ([Spacemacs: choosing themes](https://github.com/syl20bnr/spacemacs/blob/develop/doc/DOCUMENTATION.org#choosing-themes)).

1. Copy [fmind-theme.el](fmind-theme.el) to `~/.emacs.d/private/local/fmind-theme/`.
2. Add `(fmind :location local)` to `dotspacemacs-themes` in `~/.spacemacs`.
