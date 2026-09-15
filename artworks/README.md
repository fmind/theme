# Branding artwork sources

The approved design uses the original FΦ logo, actual Google Sans Bold, `fmind.dev`, and `AI Agents, MLOps & Security` within the reference's rounded blue frame. Download the finished [wallpapers](../wallpapers/README.md) or [social banners](../banners/README.md).

[All twelve variants](previews/all-variants.png) · [Reference above / adaptation below](previews/reference-comparison.png) · [Shared composition](composition.svg)

## Regenerate

```sh
mise run artwork
```

The task runs [generate.py](generate.py) with its dependency lockfile and ImageMagick. Edit this shared generator to change the design or canvas layouts. It recreates the twelve self-contained SVGs and RGB PNGs, composition, contact sheet, crop previews and [hash manifest](manifest.json). Per-platform SVGs are generated outputs; direct edits are replaced on regeneration. The bundled logo, reference banner and font make regeneration independent of external brand files or installed fonts; uv and mise supply the rendering tools.

## Fidelity

`logo.png` and `reference-banner.png` are unchanged copies of the supplied originals. The logo is embedded as its original PNG bytes and scaled proportionally, without tracing, recoloring or cropping. HarfBuzz shapes actual `GoogleSans-Bold.ttf` glyphs, including kerning, and fontTools exports their outlines so SVG viewers cannot substitute another font.

The solid frame and wordmark use the theme blue `#174ea6` from [the shared palette](../checks/palette.yaml). The tagline `#353b4e` and near-white `#fdfdfd` were sampled from the reference's nearly opaque interior regions. The reference and original logo retain their supplied colors, texture and partial transparency; generated exports composite the original logo onto the solid near-white background. Both text colors exceed 4.5:1 contrast on that background.

The supplied standalone logo differs from the banner's pictured mark in ring thickness and letter placement. Actual Google Sans Bold also differs from the reference raster lettering, particularly its `f` and apparent weight. These authentic supplied assets take priority over redrawing approximations. The longer updated tagline is smaller to fit one line. All variants preserve the internal proportions; only overall scale, placement and surrounding whitespace change.

Portrait wallpapers preserve the horizontal arrangement, giving more vertical whitespace and smaller lettering. At 360 px display width, phone tagline capitals are approximately 11 px high. Use Fit in wallpaper settings to preserve the complete panel.

## Crop evidence and limits

Primary sources checked on 2026-09-15. No social upload or live profile rendering was tested. The previews establish geometric containment; avatar overlays and responsive crops can vary by client.

- [YouTube guidance](https://support.google.com/youtube/answer/10456525?hl=en) recommends 2560 × 1440, at most 6 MB, and a central 1235 × 338 safe area at the 2048 × 1152 minimum. Scaling by 1.25 yields 1543.75 × 422.5. The entire panel fits the conservative [1543 × 422 crop](previews/youtube-mobile-crop.png). The requested brand frame is retained despite Google's advice against borders and frames.
- [X guidance](https://help.x.com/en/managing-your-account/common-issues-when-uploading-profile-photo) recommends 1500 × 500. The panel leaves 307.5 px at the left for typical avatar placement and space above and below for cropping.
- [LinkedIn guidance](https://www.linkedin.com/help/linkedin/answer/a568217/add-or-change-the-background-photo-on-your-profile) recommends 1584 × 396, PNG/JPG under 8 MB, and notes that browser dimensions affect appearance. The panel leaves approximately 372 px at the left; live responsive avatar overlap remains unverified.
- [Reddit community guidance](https://support.reddithelp.com/hc/en-us/articles/15484339588884-Banner) specifies at least 1072 × 128 desktop and 1080 × 128 mobile. The requested 1920 × 384 canvas is retained, with a smaller panel fitting the conservative [1920 × 227 central crop](previews/reddit-mobile-crop.png). This trades display size for preservation of the complete frame. Community guidance does not establish personal-profile compatibility.
- The [Bluesky profile schema](https://raw.githubusercontent.com/bluesky-social/atproto/main/lexicons/app/bsky/actor/profile.json) accepts PNG/JPEG banners up to 1,000,000 bytes. The export satisfies that cap; 1500 × 500 is the requested layout choice, and the schema does not establish crop behavior.
- [Mastodon documentation](https://docs.joinmastodon.org/user/profile/) states that headers are downscaled to 1500 × 500, matching the export. Individual server/client overlays remain untested.

## Validation

`mise run all` verifies the manifest’s source and PNG output hashes, PNG byte counts, corresponding SVG file presence and font-license file presence. It does not validate image dimensions, embedded content, encoding or crop bounds. Check regeneration separately by comparing output hashes before and after `mise run artwork`. Local checks and visual acceptance do not imply platform publication.

## Font license

`GoogleSans-Bold.ttf` is Copyright 2025 The Google Sans Project Authors (github.com/googlefonts/googlesans), as recorded in its name table, and is distributed under the [SIL Open Font License 1.1](OFL.txt). The repository MIT license does not replace this font license. The original font bytes and attribution are preserved.
