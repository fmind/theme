# Fmind for APT

Truecolor configuration for APT 3.x on Debian/Ubuntu, using native terminal escape sequences and action color references. Use a truecolor terminal with a light background.

## Installation

Copy [fmind.conf](fmind.conf) to `/etc/apt/apt.conf.d/99fmind`. APT honors `NO_COLOR` and `APT_NO_COLOR`; redirected output remains uncolored.

## Validation

After installation, inspect `apt list apt` in a truecolor terminal with a light background. Check that the package name is dark blue and the following text resets its color. Native APT behavior and transaction states require manual verification; repository checks do not run APT.
