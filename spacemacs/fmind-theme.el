;;; fmind-theme.el --- Fmind theme for Spacemacs

(deftheme fmind "Fmind light theme for Spacemacs")

(let ((class '((class color) (min-colors 89)))
      (bg "#ffffff")
      (fg "#202124")
      (panel "#f1f3f4")
      (muted "#595d62")
      (blue "#174ea6")
      (green "#0d652d")
      (red "#a50e0e")
      (selection "#d2e3fc"))
  (custom-theme-set-faces
   'fmind
   `(default ((,class (:background ,bg :foreground ,fg))))
   `(region ((,class (:background ,selection))))
   `(font-lock-comment-face ((,class (:foreground ,muted :slant italic))))
   `(font-lock-keyword-face ((,class (:foreground ,blue :weight bold))))
   `(font-lock-string-face ((,class (:foreground ,green))))
   `(font-lock-warning-face ((,class (:foreground ,red :weight bold))))))

(provide-theme 'fmind)
