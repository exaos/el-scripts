#!/bin/bash
# -*- mode: shell-script; coding: utf-8; -*-
# by Exaos Lee (exaos.lee@gmail.com)

EMACS=/usr/bin/emacs

EIDS=`pgrep emacs`
if [[ "$EIDS" ]] ; then
    echo "Emacs is running: ${EIDS}"
fi

pkill emacs

rm -f $HOME/.emacs.d/session.*

# sometimes, fix bug while fcitx works with emacs

LC_CTYPE=zh_CN.UTF-8  ${EMACS} --daemon

