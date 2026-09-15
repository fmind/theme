# Qutebrowser Fmind Light Theme

c = globals().get("c")

if c is not None:
    c.colors.webpage.preferred_color_scheme = "light"

    # Completion
    c.colors.completion.category.bg = "#f1f3f4"
    c.colors.completion.category.fg = "#202124"
    c.colors.completion.even.bg = "#ffffff"
    c.colors.completion.odd.bg = "#ffffff"
    c.colors.completion.fg = "#202124"
    c.colors.completion.item.selected.bg = "#d2e3fc"
    c.colors.completion.item.selected.fg = "#202124"

    # Statusbar
    c.colors.statusbar.normal.bg = "#ffffff"
    c.colors.statusbar.normal.fg = "#202124"
    c.colors.statusbar.url.fg = "#174ea6"

    # Tabs
    c.colors.tabs.even.bg = "#f1f3f4"
    c.colors.tabs.even.fg = "#595d62"
    c.colors.tabs.odd.bg = "#f1f3f4"
    c.colors.tabs.odd.fg = "#595d62"
    c.colors.tabs.selected.even.bg = "#ffffff"
    c.colors.tabs.selected.even.fg = "#202124"
    c.colors.tabs.selected.odd.bg = "#ffffff"
    c.colors.tabs.selected.odd.fg = "#202124"
