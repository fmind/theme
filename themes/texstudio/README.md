# TeXstudio

Fmind light syntax color profile for TeXstudio.

Format: [TeXstudio profiles](https://github.com/texstudio-org/texstudio/blob/master/utilities/manual/source/advanced.md#saveload-profile) · [format loader](https://github.com/texstudio-org/texstudio/blob/master/src/qcodeedit/lib/qformatscheme.cpp) · [format IDs](https://github.com/texstudio-org/texstudio/blob/master/utilities/qxs/defaultFormats.qxf)

## Install

1. Back up your settings with **Options** → **Save Profile...**.
2. Choose **Options** → **Load Profile...** and select [fmind.txsprofile](fmind.txsprofile). TeXstudio copies only the profile's `[formats]` keys into your configuration.

The profile sets the light-mode editor and syntax colors. TeXstudio keeps dark-mode colors in a separate `[formatsDark]` section, which this profile leaves unchanged.
