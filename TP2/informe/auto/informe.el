(TeX-add-style-hook
 "informe"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("fontenc" "T1") ("inputenc" "utf8") ("babel" "spanish")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "fontenc"
    "inputenc"
    "babel"
    "graphicx"
    "microtype"
    "xcolor"
    "amsmath"
    "amssymb"
    "mathtools"
    "xfrac"
    "booktabs"
    "hyperref"
    "siunitx")
   (TeX-add-symbols
    "todox"
    "ham"
    "spam"
    "fo")
   (LaTeX-add-xcolor-definecolors
    "red"))
 :latex)

