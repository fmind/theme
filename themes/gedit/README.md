# Fmind for Gedit

Files: [fmind.xml](fmind.xml).

Format: [libgedit-gtksourceview style scheme parser](https://gitlab.gnome.org/World/gedit/libgedit-gtksourceview/-/blob/main/gtksourceview/gtksourcestyleschemeparser.c) · [bundled schemes](https://gitlab.gnome.org/World/gedit/libgedit-gtksourceview/-/tree/main/data/style-schemes/default-style-schemes)

## Installation

Copy to `~/.local/share/libgedit-gtksourceview-300/styles/` and select Fmind in Preferences → Font & Colors. Current gedit reads style schemes through libgedit-gtksourceview, whose format (299.2 or later) requires `kind` and rejects the `version` attribute and `<author>` element; for GtkSourceView 4 or 5 apps, use the [GtkSourceView](../gtksourceview/) port.
