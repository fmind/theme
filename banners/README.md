# Fmind social banners

Upload the PNG; use the generated SVG for scalable viewing. Each layout preserves the logo on the left of the website and tagline. X, LinkedIn, Bluesky and Mastodon layouts leave extra space at the left for a profile photo.

| Platform | Pixels      | Download            | Source              |
| -------- | ----------- | ------------------- | ------------------- |
| YouTube  | 2560 × 1440 | [PNG](youtube.png)  | [SVG](youtube.svg)  |
| X        | 1500 × 500  | [PNG](x.png)        | [SVG](x.svg)        |
| LinkedIn | 1584 × 396  | [PNG](linkedin.png) | [SVG](linkedin.svg) |
| Reddit   | 1920 × 384  | [PNG](reddit.png)   | [SVG](reddit.svg)   |
| Bluesky  | 1500 × 500  | [PNG](bluesky.png)  | [SVG](bluesky.svg)  |
| Mastodon | 1500 × 500  | [PNG](mastodon.png) | [SVG](mastodon.svg) |

## Sizing and crop checks

The YouTube composition fits its central mobile safe area; Reddit keeps a smaller composition inside a shallow central crop. X, LinkedIn, Bluesky and Mastodon reserve space on the left for typical profile-photo overlays. See [platform sources, crop previews and limitations](../artworks/README.md#crop-evidence-and-limits).

Check the upload preview on desktop and mobile before saving. Responsive crops and overlays remain unverified; Reddit community guidance does not establish personal-profile compatibility. No account was changed.

The circular FΦ mark is the byte-identical original logo asset. The logo stays on the left of `fmind.dev` and `AI Agents, MLOps & Security` inside the rounded blue panel border. Royal blue `#004BBA` and dark slate `#353B4E` sit on near-white `#FDFDFD`; the text uses shaped Google Sans Bold outlines.

## Editing and export

Run `mise run artwork` from the repository root to regenerate every SVG, PNG, preview and manifest using locked dependencies and the bundled logo and Google Sans font. Edit the shared generator instead of individual generated SVGs; see [artwork sources and fidelity notes](../artworks/README.md). [Preview all twelve variants](../artworks/previews/all-variants.png).
