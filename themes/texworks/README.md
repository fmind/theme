# Fmind for TeXworks

Syntax colors for [TeXworks](https://www.tug.org/texworks/).

## Installation

Open TeXworks' resources folder from Help → Settings and Resources, then edit `configuration/syntax-patterns.txt`. Replace only its `[LaTeX]` section with [fmind.txt](fmind.txt), preserving other sections. Keep the leading spaces before hex colors: without them, TeXworks treats those rules as comments. Restart TeXworks.

This fragment uses the [native syntax-pattern format](https://github.com/TeXworks/texworks/blob/main/res/resfiles/configuration/syntax-patterns.txt). Native loading and rendering remain unverified here.
