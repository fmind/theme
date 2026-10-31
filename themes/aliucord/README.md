# Aliucord

Fmind accent theme for Aliucord's Themer plugin on Discord's light appearance. It sets the dark blue accent (links, brand buttons, mentions) and the light blue selected-channel background; other colors stay Discord's.

Format: [Themer theme spec](https://github.com/Vendicated/AliucordPlugins/blob/main/Themer/README.md) · [Themer ThemeLoader.kt](https://github.com/Vendicated/AliucordPlugins/blob/main/Themer/src/main/kotlin/dev/vendicated/aliucordplugs/themer/ThemeLoader.kt)

## Install

1. Install the [Themer](https://github.com/Vendicated/AliucordPlugins/tree/main/Themer) plugin and choose Discord's light appearance.
2. Copy [fmind.json](fmind.json) to `Aliucord/themes/` in your device's internal storage.
3. Enable **Fmind** in the Themer plugin settings.

Themer reads colors as signed ARGB integers: `-15249754` is `#174EA6` and `-2956292` is `#D2E3FC`. A native Aliucord session remains unverified.
