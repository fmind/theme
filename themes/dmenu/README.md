# Fmind for dmenu

Files: [fmind.h](fmind.h).

## Installation

Configuration destinations are relative to `~/.config` unless an absolute path or another location is specified. Merge fragments into existing settings.

Copy beside dmenu’s `config.h`; replace its complete `colors` definition with `#include "fmind.h"`, then rebuild dmenu with your normal build procedure. Choose Google Sans through its `fonts` setting. Includes normal, selected and output schemes.
