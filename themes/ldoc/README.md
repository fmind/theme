# Fmind for LDoc

Documentation theme for [LDoc](https://github.com/lunarmodules/LDoc).

Format: [LDoc html.lua custom_css](https://github.com/lunarmodules/ldoc/blob/master/ldoc/html.lua) · [default ldoc_css.lua](https://github.com/lunarmodules/ldoc/blob/master/ldoc/html/ldoc_css.lua)

## Installation

Copy [fmind.css](fmind.css) into the directory where you run `ldoc`, usually beside `config.ld`, and add `custom_css = "fmind.css"` to `config.ld`. Use the bare file name: LDoc copies it into the output directory and links it after its default `ldoc.css`, which keeps the sidebar layout. Leave `style` unset: pointing it at a directory makes LDoc copy that directory's `ldoc.css` instead of its default.
