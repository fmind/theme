# $language = "Python"
# $interface = "1.0"

# Fmind color scheme and ANSI palette for SecureCRT 8.7 or later.
# Format: VanDyke's ImportAdditionalColorSchemesIntoGlobalConfig.py example
# writes the same "ANSI Color Palettes" and "Color Schemes" global options:
# https://www.vandyke.com/support/scripting/scripting-examples/scripts/ImportAdditionalColorSchemesIntoGlobalConfig.py.txt
# Palette entry: name, then ANSI colors 0-15 as RRGGBB followed by 00.
# Scheme entry: name, flags, 8 foreground and 8 background values, palette name.
# Re-running replaces the earlier Fmind entries and keeps every other entry.

# SecureCRT injects `crt` into the script's globals.
crt = globals().get("crt")
if crt is None:
    raise SystemExit("Run fmind.py from the SecureCRT Script menu.")

NAME = "Fmind"
TEXT = "20212400"
WHITE = "FFFFFF00"
ANSI = [
    "20212400",  # black: text
    "A50E0E00",  # red
    "0D652D00",  # green
    "93490000",  # yellow: orange
    "174EA600",  # blue
    "681DA800",  # magenta: purple
    "00636D00",  # cyan: teal
    "20212400",  # white: text on a light terminal
    "595D6200",  # bright black: comment
    "A50E0E00",  # bright red
    "0D652D00",  # bright green
    "93490000",  # bright yellow: orange
    "174EA600",  # bright blue
    "681DA800",  # bright magenta: purple
    "00636D00",  # bright cyan: teal
    "20212400",  # bright white: text
]
PALETTE = ",".join([NAME] + ANSI)
SCHEME = ",".join([NAME, "010101"] + [TEXT] * 8 + [WHITE] * 8 + [NAME])


def upsert(option, entry):
    name = entry.split(",", 1)[0]
    entries = [existing for existing in crt.Config.GetOption(option) if existing.split(",", 1)[0].strip() != name]
    entries.append(entry)
    crt.Config.SetOption(option, sorted(entries, key=lambda item: item.strip().lower()))


def main():
    major_minor = crt.Version.split(" ")[0].split(".")[:2]
    if tuple(int(part) for part in major_minor) < (8, 7):
        crt.Dialog.MessageBox(
            "The Fmind color scheme needs SecureCRT 8.7 or later.\r\nThis is SecureCRT " + crt.Version + "."
        )
        return
    upsert("ANSI Color Palettes", PALETTE)
    upsert("Color Schemes", SCHEME)
    crt.Dialog.MessageBox(
        "Added the Fmind color scheme and ANSI palette.\r\nSelect Fmind under Session Options > Terminal > Appearance."
    )


main()
