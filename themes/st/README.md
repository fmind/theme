# Fmind for st

Files: [fmind.h](fmind.h).

Format: [st config.def.h](https://git.suckless.org/st/file/config.def.h.html)

## Installation

Copy beside st’s `config.h`; replace its `colorname` array and the four `defaultfg`, `defaultbg`, `defaultcs`, `defaultrcs` definitions with `#include "fmind.h"`. Rebuild using your normal st procedure. Slots 16–255 remain st’s native extended palette.
