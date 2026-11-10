# Fmind for GitHub Copilot CLI

Files: [settings.json](settings.json).

Format: [Copilot CLI configuration directory](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference)

## Installation

Use a Fmind terminal palette, then run `/settings theme default` in GitHub Copilot CLI (or `copilot config theme default`). Unlike the default `github` palette, `default` delegates output colors to the terminal's 16 ANSI slots.

[settings.json](settings.json) records the equivalent `"theme": "default"` preference for `~/.copilot/settings.json`. Merge the key into your user `settings.json` rather than overwriting existing settings or placing it in repository configuration. Tested with GitHub Copilot CLI 1.0.108.
