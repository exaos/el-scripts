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
    cd ${DEPOT_BASE}/$1
    git-annex sync $2
    cd -
}

depot_copy() {
    echo "==> Copy data to depot $2 ..."
    cd ${DEPOT_BASE}/$1
    git-annex copy --to $2 --not --in $2
    cd -
}

depot_cmd() {
    echo "==> on ($1) running ($2) ..."
    BASE=${1}
    shift 1
    CMD=${1:-git}
    shift 1
    cd ${DEPOT_BASE}/${BASE}
    echo "[base:${BASE}] \$ ${CMD} ${*} "
    ${CMD} ${*}
    cd -
}

cmd_all() {
    for d in ${DEPOTS[@]} ; do
        depot_cmd $d $@
    done
}

status_all() {
    for d in ${DEPOTS[@]} ; do
        depot_status $d $1
    done
}

sync_all() {
    for d in ${DEPOTS[@]} ; do
        depot_sync $d $1
    done
}

copy_all() {
    for d in ${DEPOTS[@]} ; do
        depot_copy $d $1
    done
}

usage() {
    echo "Usage: $0 <cmd> [<parameters>]"
    echo "Base directory: ${DEPOT_BASE}"
    echo "Handling depots: ${DEPOTS[@]}"
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
        DEST=${2:-EADEPOT}
        sync_all ${DEST}
        ;;
    cp | copy)
        DEST=${2:-EADEPOT}
        copy_all ${DEST}
        ;;
    *)
        cmd_all $@
        ;;
esac

