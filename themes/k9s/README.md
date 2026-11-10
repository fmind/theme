# Fmind for k9s

Files: [fmind.yaml](fmind.yaml).

Format: [k9s skins](https://k9scli.io/topics/skins/) · [k9s skin schema](https://github.com/derailed/k9s/blob/master/internal/config/json/schemas/skin.json) · [k9s style keys](https://github.com/derailed/k9s/blob/master/internal/config/styles.go)

## Installation

Copy `fmind.yaml` to the skins directory shown by `k9s info` (`~/.config/k9s/skins/fmind.yaml` on Linux, `~/Library/Application Support/k9s/skins/fmind.yaml` on macOS), and set `k9s.ui.skin: fmind` in `config.yaml`.
