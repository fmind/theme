# Fmind for Home Assistant

Light theme for [Home Assistant](https://www.home-assistant.io/).

Format: [Home Assistant themes](https://www.home-assistant.io/integrations/frontend/#defining-themes) · [color.globals.ts](https://github.com/home-assistant/frontend/blob/dev/src/resources/theme/color/color.globals.ts)

## Installation

Copy [fmind.yaml](fmind.yaml) into a `themes/` folder beside `configuration.yaml`, load that folder with `frontend: themes: !include_dir_merge_named themes` in `configuration.yaml`, restart Home Assistant, then select Fmind in your profile.
