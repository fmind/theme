;;; doom-fmind-theme.el --- Fmind theme for DOOM Emacs -*- lexical-binding: t; no-byte-compile: t; -*-

(require 'doom-themes)

(def-doom-theme doom-fmind
  "A light theme inspired by Google brand colors on white."

  ;; name        default   256       16
  ((bg         '("#ffffff" "#ffffff" "white"))
   (fg         '("#202124" "#202124" "black"))

   ;; These are surfaces and shades
   (bg-alt     '("#f1f3f4" "#f1f3f4" "white"))
   (base0      '("#ffffff" "#ffffff" "white"))
   (base1      '("#f1f3f4" "#f1f3f4" "white"))
   (base2      '("#f1f3f4" "#f1f3f4" "white"))
   (base3      '("#d2e3fc" "#d2e3fc" "brightwhite"))
   (base4      '("#9aa0a6" "#9aa0a6" "grey"))
   (base5      '("#595d62" "#595d62" "brightblack"))
   (base6      '("#595d62" "#595d62" "brightblack"))
   (base7      '("#202124" "#202124" "brightblack"))
   (base8      '("#202124" "#202124" "black"))
   (fg-alt     '("#595d62" "#595d62" "brightblack"))

   (grey       base4)
   (red        '("#a50e0e" "#a50e0e" "red"))
   (orange     '("#934900" "#934900" "brightred"))
   (green      '("#0d652d" "#0d652d" "green"))
   (teal       '("#00636d" "#00636d" "brightgreen"))
   (yellow     '("#e37400" "#e37400" "yellow"))
   (blue       '("#174ea6" "#174ea6" "brightblue"))
   (dark-blue  '("#174ea6" "#174ea6" "blue"))
   (magenta    '("#681da8" "#681da8" "magenta"))
   (violet     '("#681da8" "#681da8" "brightmagenta"))
   (cyan       '("#00636d" "#00636d" "cyan"))
   (dark-cyan  '("#00636d" "#00636d" "darkcyan"))

   ;; face categories
   (highlight      blue)
   (vertical-bar   base4)
   (selection      base3)
   (builtin        magenta)
   (comments       base5)
   (doc-comments   base5)
   (constants      orange)
   (functions      blue)
   (keywords       blue)
   (methods        blue)
   (operators      fg)
   (type           magenta)
   (strings        green)
   (variables      fg)
   (numbers        orange)
   (region         selection)
   (error          red)
   (warning        orange)
   (success        green))

  ;; Faces
  ((doom-modeline-bar :background blue)
   (mode-line
    :background bg-alt :foreground fg
    :box (if -modeline-pad `(:line-width ,-modeline-pad :color ,bg-alt)))
   (mode-line-inactive
    :background bg :foreground base5
    :box (if -modeline-pad `(:line-width ,-modeline-pad :color ,bg)))
   (line-number :foreground base4 :background bg)
   (line-number-current-line :foreground fg :background base1 :bold t)))

;;; doom-fmind-theme.el ends here
