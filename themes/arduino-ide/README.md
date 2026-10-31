# Arduino IDE

Fmind light theme for the legacy Arduino IDE 1.8. Arduino IDE 2.x does not read `theme.txt`; it loads VS Code themes from `~/.arduinoIDE/plugins/` ([Arduino’s instructions](https://github.com/arduino/arduino-ide/blob/main/docs/advanced-usage.md#3rd-party-themes)), so copy the [VS Code theme](../vscode/) directory there instead.

Format: [Arduino IDE 1.x theme.txt](https://github.com/arduino/Arduino/blob/master/build/shared/lib/theme/theme.txt)

## Installation

1. Locate your Arduino IDE `lib/theme/` directory (e.g. `/usr/share/arduino/lib/theme/` on Linux or inside `Arduino.app/Contents/Java/lib/theme/` on macOS).
2. Backup the existing `theme.txt`.
3. Merge the keys from this `theme.txt` into it, replacing the matching lines and keeping all other lines.
4. Restart Arduino IDE.
