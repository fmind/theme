# Fmind SDDM

Implementation checkpoint: native greeter and final keyboard-dismissal validation remain unfinished. See [TODO.md](../../../TODO.md#resume-the-sddm-checkpoint-first) before treating this component as complete.

A white SDDM login screen with user selection or manual usernames, password entry, desktop sessions, keyboard layouts, Caps Lock feedback, a clock, confirmed sleep/restart/shutdown actions, an on-screen keyboard and optional battery status. Authentication and session launch use SDDM's supplied interfaces. Empty passwords reach SDDM so the system's authentication policy decides whether they are valid.

## Installation

Install the Qt Quick, Controls 2, Layouts and Qt Virtual Keyboard modules matching your SDDM greeter's Qt major version, including the virtual-keyboard input-method plugin and its runtime dependencies. Install Google Sans system-wide so the greeter account can read it. Copy the complete [Fmind](Fmind/) directory to `/usr/share/sddm/themes/Fmind/`, including its nested `QtQuick/` directory. These files must be readable by the greeter account and writable only by an administrator.

The package defaults to Qt 6. For a Qt 5.15 greeter, change `QtVersion=5` in the installed `metadata.desktop` and `qtVersion=5` in the installed `theme.conf.user` under `[General]`. Keep those two values aligned. Qt 5 and Qt 6 use separate virtual-keyboard import declarations with the same appearance.

Add the following settings to your local SDDM configuration, normally `/etc/sddm.conf.d/fmind.conf`. Merge the environment entries with any existing `GreeterEnvironment` value; retain existing import paths after Fmind's path, separated by colons. Existing `/etc/sddm.conf` settings take precedence over configuration-directory files. See the [SDDM configuration definitions](https://github.com/sddm/sddm/blob/v0.21.0/src/common/Configuration.h) and [configuration manual](https://github.com/sddm/sddm/blob/v0.21.0/data/man/sddm.conf.rst.in).

```ini
# https://github.com/sddm/sddm/blob/v0.21.0/data/man/sddm.conf.rst.in
[General]
InputMethod=qtvirtualkeyboard
GreeterEnvironment=QML2_IMPORT_PATH=/usr/share/sddm/themes/Fmind,QML_IMPORT_PATH=/usr/share/sddm/themes/Fmind,QT_VIRTUALKEYBOARD_DESKTOP_DISABLE=1

[Theme]
Current=Fmind
```

The import paths let Qt discover Fmind's keyboard styles; the theme selects the appropriate style when opening its embedded keyboard. The keyboard inherits the installed Qt layouts and language-switch behavior. Passwords are masked, excluded from predictive learning, and cleared immediately after submission and on failure. The keyboard style omits magnified character previews.

Apply the theme on the next normal greeter start. Do not restart SDDM from a desktop session containing unsaved work. To revert, restore the previous `Current` value and remove only the Fmind-specific environment entries. This repository's checks do not install or activate the login theme.

## Optional battery status

Battery status is disabled by default so the login screen does not require Plasma on non-KDE systems. Install the battery provider matching the greeter toolkit before enabling it in the installed `theme.conf.user`:

```ini
# https://github.com/sddm/sddm/blob/v0.21.0/docs/THEMING.md
[General]
showBattery=true
batteryProvider=plasma6
```

For Plasma 6, the provider is `org.kde.plasma.private.battery` from Plasma Workspace. For Plasma 5, set `batteryProvider=plasma5`; this uses `org.kde.plasma.core` and its `powermanagement` data engine. The label shows the percentage and power connection, turns red below 20%, and disappears when no battery is present. Battery providers and the greeter must use the same Qt major version.

## Validation and limits

The retained [preview](Fmind/preview.png) uses synthetic accounts and sessions. Native Qt 5.15.8 and Qt 6.4.2 checks exercise login requests, failure recovery, session validation, power confirmation, virtual-key input and password masking. Battery presentation is checked against synthetic provider data; the real KDE battery providers remain unverified. The native SDDM process did not complete a warning-free test, and real authentication, session launch, power management, Wayland greeter operation and a deployed login screen remain unverified. See [coverage](../../../COVERAGE.md) for the exact evidence and failures.

Edit the QML and native configuration directly. Keep the two keyboard styles visually identical and refresh the synthetic package preview after visual changes. User names and provider messages render as plain text. No theme code runs shell commands, changes authentication policy or contacts remote services.
