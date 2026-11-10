# Fmind for OpenCode

Files: [fmind.json](fmind.json).

Format: [OpenCode themes](https://opencode.ai/docs/themes/) · [schema.ts](https://github.com/anomalyco/opencode/blob/dev/packages/theme/src/tui/schema.ts)

## Installation

Copy [fmind.json](fmind.json) to `~/.config/opencode/themes/fmind.json`, then select `fmind` via `Ctrl+P` → **Open settings** → **Theme** or in `~/.config/opencode/cli.json`:

```json
{
  "theme": {
    "name": "fmind",
    "mode": "light"
  }
}
```

Uses the OpenCode 2.x V2 theme format so palette colors are applied without OKLCH hue synthesis. Tested with OpenCode 2.2.6.
