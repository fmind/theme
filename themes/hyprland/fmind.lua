-- https://wiki.hypr.land/Configuring/Basics/Variables/
-- Hyprland 0.55+; load after your other appearance settings.
hl.config({
    general = {
        col = {
            active_border = "rgba(174ea6ff)",
            inactive_border = "rgba(9aa0a6ff)",
        },
    },
    decoration = {
        shadow = { color = "rgba(595d62ff)", color_inactive = "rgba(9aa0a6ff)" },
    },
    group = {
        col = {
            border_active = "rgba(174ea6ff)",
            border_inactive = "rgba(9aa0a6ff)",
            border_locked_active = "rgba(934900ff)",
            border_locked_inactive = "rgba(595d62ff)",
        },
        groupbar = {
            font_family = "Google Sans",
            -- Opaque title fills keep contrast independent of the window beneath.
            gradients = true,
            text_color = "rgba(174ea6ff)",
            text_color_inactive = "rgba(595d62ff)",
            text_color_locked_active = "rgba(934900ff)",
            text_color_locked_inactive = "rgba(595d62ff)",
            col = {
                active = "rgba(d2e3fcff)",
                inactive = "rgba(ffffffff)",
                locked_active = "rgba(feefc3ff)",
                locked_inactive = "rgba(ffffffff)",
            },
        },
    },
    misc = {
        font_family = "Google Sans",
        disable_hyprland_logo = true,
        disable_splash_rendering = true,
        background_color = "rgba(ffffffff)",
    },
})
