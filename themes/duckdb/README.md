# Fmind for DuckDB

Files: [fmind.duckdbrc](fmind.duckdbrc).

Format: [DuckDB CLI syntax highlighting](https://duckdb.org/docs/stable/clients/cli/syntax_highlighting) · [`~/.duckdbrc`](https://duckdb.org/docs/stable/clients/cli/overview)

## Installation

Append the contents of `fmind.duckdbrc` to `~/.duckdbrc`, which the DuckDB CLI runs at startup, or try it once with `duckdb -init fmind.duckdbrc`.

The file names ANSI colors, not hex values: keywords are blue, strings green, numbers yellow, comments gray and errors red. Use a Fmind terminal theme, such as [Ghostty](../ghostty/), so those names resolve to the palette. Without the file, the CLI uses fixed 256-color values that ignore the terminal theme. Tested with DuckDB 2.0.0.
