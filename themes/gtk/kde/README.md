# Fmind KDE

KDE application colors, a Plasma desktop style, Aurorae window decorations, Kvantum widgets, native cursors and a global theme with a startup splash. Ordinary surfaces stay white, selections are pale and semantic text remains readable. Components can be selected separately or together through the global theme. The remaining KDE components of the free Dracula GTK bundle are listed below.

## Color scheme

Copy [Fmind.colors](color-schemes/Fmind.colors) to `~/.local/share/color-schemes/Fmind.colors`, then select Fmind in System Settings → Colors. The scheme includes views, windows, buttons, selections, tooltips, complementary surfaces, headers, inactive headers and window-title colors. Alternate ordinary backgrounds remain white. Inactive selections retain their pale highlight, and disabled effects keep the background white and text readable.

Neutral feedback uses amber on ordinary surfaces. Inside selections it uses the main text color because KDE's derived neutral background otherwise falls below the required contrast. Verify these generated semantic backgrounds in the application, not only the RGB entries in the file.

Colors do not select an application widget style, font or icon theme. Use Google Sans for general text and Google Sans Code for fixed-width text in System Settings → Fonts. Applications that override the system palette need their own theme integration.

## Plasma style

Copy the complete `plasma/desktoptheme/Fmind/` directory to `~/.local/share/plasma/desktoptheme/Fmind/`, preserving its [metadata](plasma/desktoptheme/Fmind/metadata.json), [colors](plasma/desktoptheme/Fmind/colors), [settings](plasma/desktoptheme/Fmind/plasmarc) and SVG subdirectories. Select Fmind in System Settings → Plasma Style. Keep the installed Breeze default style: Plasma supplies its remaining control geometry and assets through the native fallback mechanism.

Fmind supplies opaque backgrounds for panels, dialogs, widgets, tooltips, toolbars and headings. Its list-item and task-button SVGs provide explicit normal, hover, selected/focused, attention, minimized and progress states, including panel orientations. Those state assets avoid inherited Breeze fills that use dark focus colors behind dark text. Blur, background contrast adjustment and adaptive transparency are disabled for this opaque style. Remaining controls use the installed Breeze assets with Fmind's colors.

The package uses the current JSON metadata format and native FrameSvg format. KDE Frameworks 5.103 was used for native loading, color evaluation and rendering. A Plasma 6/KSvg runtime, a complete Plasma desktop session, third-party widgets and arbitrary widget-style combinations remain unverified. Installing the style does not apply a desktop layout, change wallpapers or configure authentication.

## Aurorae window decorations

Copy the complete [aurorae/Fmind/](aurorae/Fmind/) directory to `~/.local/share/aurorae/themes/Fmind/`, preserving the `Fmind` folder name, [Fmindrc](aurorae/Fmind/Fmindrc), metadata and SVG files. Select Fmind in System Settings → Window Decorations. Choose Google Sans as the window-title font in the system font settings. Button order and button/border sizes remain configurable through KDE.

The frame stays white in active, inactive and maximized states. Title text and disabled controls remain readable. Close, minimize, maximize/restore, all-desktops, keep-above, keep-below, shade, help, application-menu and window-menu assets have explicit active, inactive, hover, pressed and disabled states. Toggle buttons retain a pale blue pressed fill; shade also reverses its arrow. Close uses a pale red hover/pressed fill. The menu SVGs are available to newer Aurorae engines; older engines render their native application icon instead. A control still depends on the application and window manager exposing that action.

The top and side margins disappear when maximized so controls reach the screen edges. One pixel remains below maximized buttons to accommodate Aurorae's integer rounding at larger button sizes. The theme draws square, opaque frames without shadows or blur. Its native SVG format and installation paths follow [KDE's Aurorae documentation](https://develop.kde.org/docs/plasma/aurorae/).

Native loading, frame/button rendering and all Aurorae border/button size combinations were checked with KWin 5.27.5 sources, KDE Frameworks 5.103 and Qt 5.15.8. A full KWin/X11 session stopped on an upstream QML module-registration warning before window interaction could be verified. Plasma 6/KSvg remains unverified.

## Kvantum widget theme

Install Kvantum for the Qt major version used by your applications. In Kvantum Manager, install the complete [kvantum/Fmind/](kvantum/Fmind/) folder and select Fmind. It contains [Fmind.kvconfig](kvantum/Fmind/Fmind.kvconfig), [Fmind.svg](kvantum/Fmind/Fmind.svg) and the matching [KDE color scheme](kvantum/Fmind/Fmind.colors). For manual installation, copy that folder to `~/.config/Kvantum/Fmind/`, then select Fmind in Kvantum Manager.

Select Kvantum as the application/widget style in KDE System Settings or LXQt Appearance. On other desktops, select it through your Qt configuration utility. For a single application that accepts Qt's standard style option, run `your-app -style kvantum`. These routes follow the [upstream installation guide](https://github.com/tsujan/Kvantum/blob/master/Kvantum/INSTALL.md). Restart applications after changing the theme, and select Google Sans/Google Sans Code in the system font settings.

The theme covers buttons, entries, combos, spin boxes, checks/radios, tabs, menus, tooltips, toolbars, trees/tables, sliders, scrollbars, progress bars, dials, dock panels, MDI windows and their controls. Ordinary backgrounds, including alternate rows and the MDI workspace, stay white. Selection and pressed states use pale blue, progress uses pale green, and disabled text remains readable. Shadows, blur and window/menu opacity reduction are disabled. Kvantum styles Qt widgets; application-specific custom painting and Qt Quick controls may require separate integrations.

Native testing used Kvantum 1.0.7 and Qt 5.15.8 under isolated Xvfb at 100%, 150% and 200% scaling in both layout directions. Palette checks, control-state renders and widget state changes pass. SVG tracing confirms that the exercised controls use Fmind's assets. Qt 6, a complete KDE/LXQt session and every application-specific rendering path remain unverified.

## Global theme and startup splash

Install the Fmind color scheme, Plasma style, Aurorae decorations, Kvantum theme and cursors using this guide. Install Google Sans and Google Sans Code, then select Fmind in Kvantum Manager. The global theme selects the Kvantum widget engine; KDE does not use this package to change Kvantum Manager's active theme.

Copy the complete [plasma/look-and-feel/Fmind/](plasma/look-and-feel/Fmind/) directory to `~/.local/share/plasma/look-and-feel/Fmind/`, preserving its metadata, defaults, colors, QML and previews. Select Fmind in System Settings → Global Theme and apply the available appearance components. The package selects Fmind colors, Plasma style, Aurorae decorations, cursors, fonts and startup splash, plus the Kvantum widget engine. It contains no desktop layout, wallpaper or icon selection and no remote package dependencies. Install its companion packages before applying it.

The package contains metadata for Plasma 5 and 6 look-and-feel formats; metadata parity does not establish runtime support. To use only its startup screen, select Fmind in System Settings → Splash Screen. The splash shows dark text and a blue activity marker on white; the marker follows Plasma's stage changes without estimating a completion percentage. Its [package preview](plasma/look-and-feel/Fmind/contents/previews/preview.png) is a native rendering of the splash, not a screenshot of an entire desktop.

KDE Frameworks 5.103 loads the package and defaults, and Plasma 5.27.5 completes its native KSplash test without warnings. The splash also renders in both Qt 5.15.8 and Qt 6.4.2 at multiple viewport sizes and scale factors. The look-and-feel package also includes native Plasma 5 components for the [lock screen](plasma/look-and-feel/Fmind/contents/lockscreen/LockScreen.qml) with clock, date and masked password entry, the [logout screen](plasma/look-and-feel/Fmind/contents/logout/Logout.qml) with session actions and countdown timer, and the [OSD](plasma/look-and-feel/Fmind/contents/osd/Osd.qml) with volume and brightness indicators. The Plasma 5.27 session interfaces remain experimental and require isolated native acceptance for authenticator conversations, capability-gated logout signals, cancellation and OSD properties. See [manual session validation](plasma/look-and-feel/Fmind/contents/README.md). Repository checks do not exercise session behavior. All surfaces remain pure white with dark charcoal text and pale blue accents. Full Global Theme application in a desktop session, a Plasma 6 package loader and the Plasma 6 KSplash process remain unverified.

## Cursor theme

Copy the complete [cursors/Fmind/](cursors/Fmind/) directory to `~/.local/share/icons/Fmind/`, preserving its symbolic links, then select Fmind in System Settings → Cursors. The package includes 113 names at six sizes, with twelve-frame wait/progress animations. See the [cursor guide](cursors/README.md) for coverage, toolkit aliases, installation alternatives and native compilation instructions.

## Bundle checklist

The [free Dracula KDE directory](https://github.com/dracula/gtk/tree/master/kde) includes additional independent packages. Its blue/purple and translucent/solid variants are coverage references; Fmind uses one consistent light palette and opaque ordinary surfaces.

- [x] KDE application color scheme.
- [x] Plasma desktop style, including opaque backgrounds and state assets.
- [x] Aurorae window decorations.
- [x] Kvantum widget theme.
- [x] Global themes and splash screens for Plasma 5 and 6.
- [ ] [Plasma 5 lock-screen, logout and OSD components](plasma/look-and-feel/Fmind/contents/) from the reference bundle.
- [x] Cursor theme.
- [ ] SDDM login-screen theme.

The desktop bundle remains experimental until native session and SDDM acceptance is complete. Existing historical component checks do not certify the current full desktop bundle.

## Maintenance

Edit the native files directly. Keep the color groups in the application scheme and Plasma `colors` file aligned; the Plasma copy intentionally omits application color-effect groups. Keep Kvantum’s bundled `Fmind.colors` and the global theme’s `contents/colors` identical to the KDE application scheme. Refresh the global theme’s splash preview from a native QML render when its appearance changes. Update the Plasma package metadata version when changing its SVGs so Plasma can invalidate its cached assets. Checks isolate their configuration and caches, and never install themes into a user profile.
