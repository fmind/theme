# tint2

Fmind theme for [tint2](https://gitlab.com/o9000/tint2).

Format: [tint2.md](https://gitlab.com/o9000/tint2/-/blob/master/doc/tint2.md) · [config.c](https://gitlab.com/o9000/tint2/-/blob/master/src/config.c)

## Install

Merge the settings from [tint2rc](tint2rc) into `~/.config/tint2/tint2rc`, then reload tint2 with `killall -SIGUSR1 tint2`. tint2 has no include directive. The file starts a new background, so set `panel_background_id` to that background's position in your config.
