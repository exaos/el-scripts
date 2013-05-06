#!/bin/bash
# Check my configurations

OS_TYPE=`uname -s | tr '[A-Z]' '[a-z]'`
if [[ "${OS_TYPE}" = cygwin* ]] || [[ "${OS_TYPE}" = msys ]] || [[ "${OS_TYPE}" = mingw* ]]
then
    export WORKSPACE=/d/Exaos/Workspace
else
    export WORKSPACE=$HOME/Workspace
fi

abs_path () {
    if [ -d $1 ]; then
	TMPDIR=$1
    else
	TMPDIR=`dirname $1`
    fi
    PSTR=`cd ${TMPDIR} && pwd -P`
    echo $PSTR
}

chk_cfg_emacs () {
    [[ ! -d ${WORKSPACE}/exaos/myconfig/emacs/ ]] && exit 1

    echo "============ [DIFF] my-init.el ============"
    diff ${WORKSPACE}/exaos/myconfig/emacs/my-init.el $HOME/.emacs.d/my-init.el
    echo "============ [DIFF] my-face.el ============"
    diff ${WORKSPACE}/exaos/myconfig/emacs/my-face.el $HOME/.emacs.d/my-face.el

    [[ ! -f ${WORKSPACE}/exaos/daily/myorg/my-org.el ]] && exit 1
    echo "============ [DIFF] my-org.el ============="
    diff ${WORKSPACE}/exaos/daily/myorg/my-org.el $HOME/.emacs.d/my-org.el
}

case "$1" in
    emacs)
	chk_cfg_emacs
	;;
    *)
	echo "Check my configurations"
	;;
esac
