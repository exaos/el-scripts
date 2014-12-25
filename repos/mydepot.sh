#!/bin/bash
# -*- mode: shell-script; coding: utf-8; -*-
# by Exaos Lee (exaos.lee@gmail.com)

DEPOT_BASE=${DEPOT_BASE:-/data/depot}
DEPOT_DISK=${DEPOT_DISK:-EADEPOT}
DEPOT_BOTS=${DEPOT_BOTS:-"Job Personal Topics"}

depot_status() {
    echo "==> [${DEPOT_BASE}: $1] \$ Status:"
    cd ${DEPOT_BASE}/$1
    git status
    cd ${OLDPWD}
}

depot_sync() {
    echo "==> [${DEPOT_BASE}: $1] \$ sync with $2 ..."
    cd ${DEPOT_BASE}/$1
    git-annex sync $2
    cd ${OLDPWD}
}

depot_copy() {
    echo "==> [${DEPOT_BASE}: $1] \$ Copy data to depot $2 ..."
    cd ${DEPOT_BASE}/$1
    git-annex copy --to $2 --not --in $2
    cd ${OLDPWD}
}

depot_cmd() {
    echo "==> [${DEPOT_BASE}: $1] \$ $2"
    BASE=${1}
    shift 1
    CMD=${1:-git}
    shift 1
    cd ${DEPOT_BASE}/${BASE}
    echo "[base:${BASE}] \$ ${CMD} ${@}"
    ${CMD} "${@}"
    cd ${OLDPWD}
}

cmd_all() {
    for d in ${DEPOT_BOTS} ; do
        depot_cmd $d $@
    done
}

status_all() {
    for d in ${DEPOT_BOTS} ; do
        depot_status $d $1
    done
}

sync_all() {
    for d in ${DEPOT_BOTS} ; do
        depot_sync $d $1
    done
}

copy_all() {
    for d in ${DEPOT_BOTS} ; do
        depot_copy $d $1
    done
}

usage() {
    echo "Usage: $0 <cmd> [<parameters>]"
    echo "Depot base path: ${DEPOT_BASE}"
    echo "Archive disk:    ${DEPOT_DISK}"
    echo "Handling depots: ${DEPOT_BOTS}"
    echo "Commands: status sync <cmd...>"
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
        DEST=${2:-${DEPOT_DISK}}
        sync_all ${DEST}
        ;;
    cp | copy)
        DEST=${2:-${DEPOT_DISK}}
        copy_all ${DEST}
        ;;
    *)
        cmd_all "$@"
        ;;
esac

