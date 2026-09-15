# Fmind MySQL Workbench

Light theme syntax highlighting for the MySQL Workbench SQL query editor.

## Install

1. Locate your MySQL Workbench installation's data directory (e.g. `/usr/share/mysql-workbench/data/` or `C:\Program Files\MySQL\MySQL Workbench X.X\data\`).
2. Back up the existing `code_editor.xml` file.
3. Replace the `<language name="SCLEX_MYSQL">` block in `code_editor.xml` with the contents of [code_editor.xml](code_editor.xml).
4. Restart MySQL Workbench to apply the new styling.
