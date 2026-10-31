# Fmind for Neiki's Editor

Light theme for [Neiki's Editor](https://github.com/neikiri/neiki-editor) 3.14.0 and later.

Format: [Neiki's Editor themes](https://github.com/neikiri/neiki-editor#themes) · [theme loader](https://github.com/neikiri/neiki-editor/blob/main/src/neiki-editor.js)

## Installation

1. Copy [fmind.json](fmind.json) and [fmind.css](fmind.css) into a `fmind/` folder inside the editor's `themes/` folder (or the folder set by `themesUrl`).
2. Add `"fmind/fmind.json"` to the `themes` array of that folder's `index.json`.
3. Choose **Fmind** in the toolbar's theme selector, pass `theme: 'fmind'` when creating the editor, or call `editor.setTheme('fmind')`.
