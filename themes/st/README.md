# Fmind for st

Files: [fmind.h](fmind.h).

## Installation

Merge fragments into existing settings.

Copy beside st’s `config.h`; replace its `colorname` array and the four `defaultfg`, `defaultbg`, `defaultcs`, `defaultrcs` definitions with `#include "fmind.h"`. Rebuild using your normal st procedure. Slots 16–255 remain st’s native extended palette.
