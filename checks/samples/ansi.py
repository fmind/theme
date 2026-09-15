"""Print synthetic ANSI background cases for visual inspection in a terminal."""

print("ANSI foreground/background compatibility (inspect in Ghostty)")
print("\x1b[37;40m White on black must remain visible \x1b[0m")
print("\x1b[37;41m White on red must remain visible \x1b[0m")
print("Each row is a background; columns are the 16 foreground slots.")
for background in range(16):
    print(f"{background:2} ", end="")
    for foreground in range(16):
        print(f"\x1b[38;5;{foreground};48;5;{background}m {foreground:02} \x1b[0m", end="")
    print()
