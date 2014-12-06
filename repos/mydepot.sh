#!/bin/bash
# -*- mode: shell-script; coding: utf-8; -*-
# by Exaos Lee (exaos.lee@gmail.com)

DEPOT_BASE=${DEPOT:-/data/depot}
DEPOTS=(Job Personal Topics)

depot_status() {
    echo "==> Status: $1"
    cd ${DEPOT_BASE}/$1
    git status
    cd -
}

depot_sync() {
    echo "==> Sync $1 with $2 ..."
    cd ${DEPOT_BASE}$1
    git annex sync $2
    cd -
}

status_all() {
    for d in ${DEPOTS[@]} ; do
        depot_status $d
    done
}

sync_all() {
    for d in ${DEPOTS[@]} ; do
        depot_sync $d $1
    done
}

usage() {
    echo "Usage: $0 <cmd> [<parameters>]"
    echo "Base depot directory: ${DEPOT_BASE}"
    echo "Handling depots: ${DEPOTS[@]}"
}

if [[ -z "$1" ]]; then
    usage
    exit 0
fi

case "$1" in
    st | status)
        status_all
        ;;
    sync)
        DEST=${2:-EADEPOT}
        echo ${DEST}
        # sync_all ${DEST}
        ;;
    *)
        usage
        ;;
esac
