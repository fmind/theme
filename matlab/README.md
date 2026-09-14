# Fmind for MATLAB

For R2025a and later, install [MathWorks MATLAB Color Theme Extensions](https://github.com/mathworks/matlab-color-theme-extensions). From that extension's directory, run the following with the absolute path to this theme:

```matlab
import_scheme('/path/to/fmind/theme/matlab/fmind.json');
```

The JSON selects the Light desktop theme and includes MATLAB syntax, output, analyzer and variable highlights, plus all 15 other language sections from the extension's template. It leaves smart indentation settings out of the import. Set Google Sans Code under MATLAB's font settings and Google Sans for general text where supported.

For older releases, install [MATLAB Schemer](https://github.com/scottclowe/matlab-schemer), run `schemer_import`, and choose `fmind.prf`. Restart MATLAB for preferences that are read at startup. This legacy file styles the editor and Command Window; it does not replace every desktop widget or plotting palette.

The current JSON schema is adapted from MathWorks' template; its BSD notice is retained in `LICENSE`. Both formats have offline palette and structure checks. Importing and rendering in MATLAB require a licensed target installation and have not been verified here.
