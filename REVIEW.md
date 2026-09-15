# Release review

Reviewed on 2026-09-15 against the working candidate, including the pre-existing staged catalog expansion. The review covers source files, offline tests, palette design, catalog accounting, documentation and delivery automation. It does not certify 483 native applications.

## Findings

1. **P1 — functional parity is not achieved.** All 472 entries in the live [free Dracula catalog](https://draculatheme.com/) are represented, but file existence was incorrectly reported as complete validated support. Minecraft contains only package metadata; Aseprite lacks its native sheet and style definitions. Their installation instructions now identify these as incomplete drafts. Adobe’s JSON-only reference now has a native ASE swatch library, checked against its source colors; Adobe desktop import remains unverified. Anytype’s invented JSON schema was replaced with native custom CSS and actual text/surface contrast checks; native app acceptance remains pending. Other experimental ports need native format review and acceptance; these examples are not an exhaustive defect list.
1. **P1 — published version conflict.** The old phosphor theme already has a published v1.0.0 release, and remote tags extend through v2.2.0. This redesign needs a new version. Reusing v1.0.0 would change an existing release’s meaning and break reproducibility.
1. **P2 — tests overstate their coverage.** Some additional-port tests only parse a document, search a string or compare a hard-coded color pair. They do not establish that the application loads the file or uses those colors. The native acceptance checklist has been reopened; the test suite remains useful for regressions within its stated boundary.
1. **P2 — desktop acceptance remains incomplete.** SDDM keyboard dismissal, current native loading, scaling and session-provider contracts remain pending. Historical GTK/KDE results in COVERAGE.md were not rerun as a full desktop campaign.
1. **P2 — repository metadata described the old theme.** The old phosphor description and topics were replaced with light-theme metadata, with the README-based GitHub Pages site as the homepage. Pages deployment is performed by CI after the gate passes.

## Palette assessment

The palette is coherent for a light theme: all 15 [Google News hex values](https://partnermarketinghub.withgoogle.com/brands/google-news/visual-identity/color-palette/) are retained. White provides the canvas; custom dark gray and dark orange preserve readable comments and literals; purple and teal separate types and information. The Google page has inconsistent RGB labels, so the exact hex values are used.

Dark shades are appropriate for text, pale shades for selection and diff backgrounds, and bright shades for accents with contrasting labels. The existing contrast tests exercise syntax across the documented surfaces. This is a design contract, not proof that every experimental port implements it. Color alone should not carry diagnostics or state: keep labels, glyphs, outlines and bold emphasis.

ANSI palettes deliberately use dark foregrounds even in slots called white. This works for foreground text on a light terminal; arbitrary ANSI backgrounds still require a terminal contrast safeguard or application overrides. See VALIDATION.md. Bright brand colors should not replace the darker syntax colors merely to increase their usage.

Claude Code’s configuration now selects `light-ansi` instead of ordinary `light`, matching the intended terminal palette inheritance. Its installation instructions use the native `/theme` selector.

## Simplicity decisions

- Keep native files directly editable and preserve the 20 core consumer paths.
- Use README as the sole website content source; one small Python renderer builds a static page. No separate documentation framework or duplicated site content.
- Keep explicit semantic version tags. Automatic version bumps and marketplace publishing add no benefit to the current delivery model.
- Keep uncertain ports labeled experimental and known incomplete drafts visible. Do not delete the user’s staged work to make the coverage number look cleaner.
- Use exact project tool pins and the shared installed baseline; isolate the project from unrelated global tool-install failures.

## Evidence boundary

The initial offline gate passed 375 tests. Final validation is recorded in VALIDATION.md. Local validation, exact-commit hosted CI, Pages deployment and a published release are separate results. Additional Windows/macOS applications, hosted app interfaces, hardware and game runtimes remain unverified. See TODO.md for the open acceptance work.
