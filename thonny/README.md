# Fmind for Thonny

Create a wheel from this directory:

```sh
uv build --wheel .
```

In Thonny, open Tools → Manage plug-ins → Install from local file, and select the wheel in `dist/`. Restart Thonny. Under Tools → Options → Theme & Font, select **Fmind** for both UI theme and syntax theme. Choose **Google Sans Code** as the editor font. General UI text follows Thonny's `TkDefaultFont`; configure Google Sans through the operating system's font settings.

The plugin provides the editor, shell, debugger, search, ANSI tags and a light widget theme. It reuses Thonny's built-in Clean/Enhanced Clam widget layouts with Fmind colors. ANSI background tags use pale fills so output remains readable. It registers themes without selecting them or changing user preferences.

Targets Thonny 4.1–5.x. Native registration and Tk style checks are separate from full platform and debugger rendering.
