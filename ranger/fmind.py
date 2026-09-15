# Ranger Fmind colorscheme
# Colors: #ffffff, #202124, #174ea6, #0d652d, #a50e0e

try:
    from ranger.gui.color import blue, bold, default_colors, green, red
    from ranger.gui.colorscheme import ColorScheme
except ImportError:
    ColorScheme = object
    bold = blue = green = red = 0
    default_colors = (0, 0, 0)


class Fmind(ColorScheme):
    def use(self, context):
        fg, bg, attr = default_colors

        if context.reset:
            return default_colors

        if context.directory:
            attr |= bold
            fg = blue
        elif context.executable and not any((context.media, context.container)):
            attr |= bold
            fg = green
        elif context.error:
            attr |= bold
            fg = red

        return fg, bg, attr
