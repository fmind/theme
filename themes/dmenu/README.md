# Fmind for dmenu

Files: [fmind.h](fmind.h).

Format: [dmenu config.def.h](https://git.suckless.org/dmenu/file/config.def.h.html)

## Installation

Copy beside dmenu’s `config.h`; replace its complete `colors` definition with `#include "fmind.h"`, then rebuild dmenu with your normal build procedure. Choose Google Sans through its `fonts` setting. Includes normal, selected and output schemes.
