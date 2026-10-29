# Fmind qBittorrent

A high-contrast light theme for the qBittorrent desktop app.

## Install

1. Compile [resources.qrc](resources.qrc) into a `.qbtheme` bundle from this directory:
   ```sh
   rcc -binary -o fmind.qbtheme resources.qrc
   ```
2. Open qBittorrent and navigate to **Tools** → **Options** → **Behavior**.
3. Under **Interface**, check **Use custom UI Theme**.
4. Select the compiled `fmind.qbtheme` file and click **Apply**.
5. Restart qBittorrent to complete the setup.
