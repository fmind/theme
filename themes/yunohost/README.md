# Fmind for YunoHost

Light portal theme for [YunoHost](https://yunohost.org/).

Format: [YunoHost portal custom_css](https://github.com/YunoHost/yunohost/blob/dev/share/config_domain.toml) · [portal custom.css route](https://github.com/YunoHost/yunohost/blob/dev/conf/nginx/yunohost_sso.conf.inc) · [DaisyUI 4 color variables](https://github.com/saadeghi/daisyui/blob/v4.12.10/src/theming/index.js)

## Installation

Requires YunoHost 12 or later. In the webadmin, open **Domains** > your top-level domain > **Features**, paste [fmind.css](fmind.css) into **Custom CSS stylesheet** and save. YunoHost writes it to `/usr/share/yunohost/portal/customassets/<domain>.custom.css` and serves it to the portal as `/yunohost/sso/customassets/custom.css`. It overrides every portal color theme.
