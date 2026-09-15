# Fmind for Claude Code

Use a Fmind terminal palette, then run `/theme` in Claude Code and select **Light (ANSI colors only)**. This preserves the terminal’s 16-color palette. Ordinary Light mode can use its own colors.

[config.json](config.json) records the equivalent `light-ansi` preference. Prefer the native `/theme` command to editing Claude’s user configuration by hand. Do not put this fragment in project settings or overwrite an existing configuration.

This integration covers ANSI terminal colors, not Claude web or desktop. Arbitrary backgrounds still depend on terminal contrast safeguards.

[Official terminal configuration](https://code.claude.com/docs/en/terminal-config).
