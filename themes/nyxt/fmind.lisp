;; Fmind theme for Nyxt browser
(in-package #:nyxt)

(define-configuration browser
  ((theme (make-instance 'theme:theme
                         :background-color "#ffffff"
                         :on-background-color "#202124"
                         :primary-color "#174ea6"
                         :on-primary-color "#ffffff"
                         :secondary-color "#f1f3f4"
                         :on-secondary-color "#202124"
                         :accent-color "#174ea6"))))
