# Fmind for Anytype

Experimental custom CSS for Anytype’s light appearance.

Format: [Anytype color variables](https://github.com/anyproto/anytype-ts/blob/develop/src/scss/_vars.scss) · [Anytype custom.css loader](https://github.com/anyproto/anytype-ts/blob/develop/electron/js/util.js)

1. Choose the built-in light appearance in Anytype.
1. Open the working directory shown in Anytype’s application menu. Merge [custom.css](custom.css) into its `custom.css` file.
1. Use **Apply custom CSS**, then restart Anytype if needed.

The stylesheet uses the native color properties referenced by the [upstream Anytype port](https://github.com/dracula/anytype/blob/main/custom.css) and its [installation instructions](https://github.com/dracula/anytype/blob/main/INSTALL.md). It covers ordinary text, surfaces, controls, selection and links. A current native Anytype session remains unverified. Dark appearance and arbitrary content colors are outside this port’s scope.
