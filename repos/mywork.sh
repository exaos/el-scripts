#!/bin/bash

OS_TYPE=`uname -s | tr '[A-Z]' '[a-z]'`
WORKSPACE=${WORKSPACE:-$HOME/Laborejo}
VLREPOS=${VLREPOS:-/data/repos/00-local/vivodo}

abs_path () {
    if [ -d $1 ]; then
	TMPDIR=$1
    else
	TMPDIR=`dirname $1`
    fi
    PSTR=`cd ${TMPDIR} && pwd -P`
    echo $PSTR
}

#### Repositories monitered
repos=(
    # ${WORKSPACE}/doc/mysite
    ${WORKSPACE}/scripts
    ${WORKSPACE}/settings
    # ${WORKSPACE}/utils/emacs/dotspacemacs
    # ${WORKSPACE}/utils/emacs/emacs-starter-vl
    ${WORKSPACE}/utils/emacs/vl_prelude
    ${WORKSPACE}/vivo
)

sync_repo () {
    [[ "$#" -ne 2 ]] && exit 1

    echo "Working on $1 ..."
    echo "==============================="
    cd "$1"
    # First: pull
    echo "Fetch from $2 ..."
    git fetch -t "$2"
    echo "Pull recent updates from $2 ..."
    git pull "$2"
    # Then: push
    echo "-------------------------------"
    echo "Push local updates to $2 ..."
    git push --all "$2"
    echo "Push tags to $2 ..."
    git push --tags "$2"
    echo
}

sync_host () {
    if [ "$1" != "path" ]; then
	RREPO_ROOT="${1}:Repos"
    else
	if [ -z "$2" ] ; then
            lrpath=${VLREPOS}
	else
	    lrpath="$2"
	fi
	RREPO_ROOT=`abs_path $lrpath`
    fi
    if [ -z "${RREPO_ROOT}" ]; then
	echo "WARNING: Incorrect repositories root path!"
	exit 1
    fi
    echo "+-------------------------------------------------------+"
    echo "|  Syncing local repositories with ${RREPO_ROOT} ..."
    echo "+-------------------------------------------------------+"

    for repo in ${repos[@]} ; do
	r_base=`basename $repo | tr [A-Z] [a-z]`
	sync_repo $repo ${RREPO_ROOT}/${r_base}.git
    done
}

## git on repos
repos_git () {
    for repo in ${repos[@]}; do
	echo "Running git $@ on $repo ..."
	echo "--------------------------------------------------------"
	cd $repo
	if [[ -z "$1" ]] ; then
	    git status
	else
	    git $@
	fi
	echo
    done
}

## list all repos
repos_list () {
    for repo in ${repos[@]}; do
	echo $repo
    done
}

##########################################################
if [[ -z "$1" ]]; then
    echo "Usage: $0 <cmd> [<parameters>]"
    cat <<EOF
Commands:
  + <l|list>         --  list monitored repositories
  + <p|path> <path>  --  sync repos with local repositories
  + <r|remote> <[user@]hostname>
                     --  sync repos with [user@]hostname
  + [g|git] <cmd>    --  git commands on repos
EOF
    exit 0
fi

case "$1" in
    l | list)
	repos_list
	;;
    p | path)
	sync_host path $2
	;;
    r | remote)
	sync_host $2
	;;
    g | git)
	shift
	repos_git $@
	;;
    *)
	repos_git $@
	;;
esac
