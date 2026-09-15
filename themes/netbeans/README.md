# Fmind for NetBeans

This native Fonts & Colors profile covers 27 MIME types, shared syntax, editor highlights and debugger annotations. Select a light look and feel under Tools → Options → Appearance; the profile styles editor content.

From this `netbeans/` directory, create the native import archive:

```sh
zip -r ../fmind-netbeans.zip config enabledItems.info
```

In NetBeans, open Tools → Options → Fonts & Colors → Import, choose that archive, and select only Fonts & Colors → Fmind. Apply the Fmind profile. Its default font is Google Sans Code; install the font or choose another font in this panel.

The archive contains only this profile and its selection attribute. It does not contain the reference export’s keymap, module settings, spellchecker settings, old build metadata or user directory. To install without an archive, copy the `Fmind` profile directories under `config/Editors/` into the same locations in your NetBeans user directory, then select Fmind in Fonts & Colors. Help → About shows the active user directory.

Native color definitions are adapted from the free Dracula NetBeans port; its MIT notice is retained in `LICENSE`.
