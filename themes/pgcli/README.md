# Fmind for pgcli

Files: [fmind.config](fmind.config).

Format: [pgcli configuration](https://www.pgcli.com/config) · [prompt_toolkit styling](https://python-prompt-toolkit.readthedocs.io/en/stable/pages/advanced_topics/styling.html)

## Installation

Merge the keys of `fmind.config` into `~/.config/pgcli/config`: set `syntax_style` in `[main]` and replace the entries of `[colors]`.

The file themes the completion menu, toolbar, search, selection, query syntax and result headers. pgcli applies the `pygments.*` entries to the query and also writes one harmless `Unhandled style / class name` line per entry to its log file.

Checked with pgcli 4.7.1 by loading the file through pgcli's style functions; not tested against a live database session.
