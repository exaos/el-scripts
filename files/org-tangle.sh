#!/bin/sh
# -*- mode: shell-script -*-
#
# tangle files with org-mode
#
DIR=`pwd`
FILES=""

# wrap each argument in the code required to call tangle on it
for j in $@; do
    FILES="$FILES \"$j\""
done

emacs -Q --batch \
    --eval \
"(progn
(add-to-list 'load-path (expand-file-name \"$HOME/.emacs.d/site-lisp/org/\"))
(require 'org) (require 'org-exp) (require 'ob) (require 'ob-tangle)
(mapc (lambda (file)
         (find-file (expand-file-name file \"$DIR\"))
         (org-bable-tangle)
         (kill-buffer)) '($FILES)))" 2>&1 | grep tangled
