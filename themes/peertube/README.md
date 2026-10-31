# Fmind for PeerTube

Light theme for [PeerTube](https://joinpeertube.org/) 7.3 or later, packaged as the `peertube-theme-fmind` theme plugin: [package.json](package.json) declares [fmind.css](fmind.css).

Format: [PeerTube theme plugins and CSS variables](https://docs.joinpeertube.org/contribute/plugins#css-variables)

## Installation

1. Copy this directory to the PeerTube server.
2. Install it as an administrator, using its absolute path on the server: `peertube-cli plugins install --path /absolute/path/to/peertube`. Server-side installs can use `npm run plugin:install -- --plugin-path /absolute/path/to/peertube`, as described in [PeerTube's tools documentation](https://docs.joinpeertube.org/maintain/tools).
3. Select **Fmind** in the **Theme** field of the administration's **Platform customization** page for the whole instance, or in the **Interface** section of a user's account settings.
