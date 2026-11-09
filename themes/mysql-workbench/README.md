# Fmind for MySQL Workbench

Light theme syntax highlighting for the MySQL Workbench SQL query editor.

Format: [MySQL Workbench code_editor.xml](https://github.com/mysql/mysql-workbench/blob/8.0/res/wbdata/code_editor.xml)

## Installation

1. Locate your MySQL Workbench installation's data directory (e.g. `/usr/share/mysql-workbench/data/` or `C:\Program Files\MySQL\MySQL Workbench X.X\data\`).
2. Back up the existing `code_editor.xml` file.
3. In the `<language name="SCLEX_MYSQL">` block of `code_editor.xml`, replace the `<style>` lines whose IDs appear in [code_editor.xml](code_editor.xml), and add the ones the block lacks. Keep the block's `<property>`, `<setting>` and `<keywords>` entries.
4. Restart MySQL Workbench to apply the new styling.
