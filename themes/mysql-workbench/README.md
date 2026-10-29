# Fmind MySQL Workbench

Light theme syntax highlighting for the MySQL Workbench SQL query editor.

## Install

1. Locate your MySQL Workbench installation's data directory (e.g. `/usr/share/mysql-workbench/data/` or `C:\Program Files\MySQL\MySQL Workbench X.X\data\`).
2. Back up the existing `code_editor.xml` file.
3. In the `<language name="SCLEX_MYSQL">` block of `code_editor.xml`, replace only the `<style>` lines for the IDs listed in [code_editor.xml](code_editor.xml) with those lines. Keep the block's `<property>`, `<setting>` and `<keywords>` entries.
4. Restart MySQL Workbench to apply the new styling.
