# Fmind Oracle SQL Developer

Clean light theme for Oracle SQL Developer code and PL/SQL editors.

## Install

1. Locate your Oracle SQL Developer configuration directory (e.g. `~/.sqldeveloper/systemX.X.X/o.sqldeveloper/` or `%APPDATA%\SQL Developer\systemX.X.X\o.sqldeveloper\`).
2. Open `dtcache.xml` in an editor.
3. Locate `<Value class="java.util.Map" key="editor-syntax-colors">` and paste the contents of [Fmind.xml](Fmind.xml) inside `<Value class="java.util.Map">`.
4. Launch Oracle SQL Developer, go to **Tools** → **Preferences** → **Code Editor** → **PL/SQL Syntax Colors**, and select **Fmind** from the **Scheme** drop-down.
