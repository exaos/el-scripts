#!/bin/bash
# Check my configurations

OS_TYPE=`uname -s | tr '[A-Z]' '[a-z]'`
if [[ "${OS_TYPE}" = cygwin* ]] || [[ "${OS_TYPE}" = msys ]] || [[ "${OS_TYPE}" = mingw* ]]
then
    export VIVO_BASE=/d/Exaos/Workspace/vivodo
else
    export VIVO_BASE=$HOME/Workspace/vivodo
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
    [[ ! -d ${VIVO_BASE}/myconfig/emacs/ ]] && exit 1

    echo "============ [DIFF] my-init.el ============"
    diff ${VIVO_BASE}/myconfig/emacs/my-init.el $HOME/.emacs.d/my-init.el
    echo "============ [DIFF] my-face.el ============"
    diff ${VIVO_BASE}/myconfig/emacs/my-face.el $HOME/.emacs.d/my-face.el

    [[ ! -f ${VIVO_BASE}/vivo/myorg/my-org.el ]] && exit 1
    echo "============ [DIFF] my-org.el ============="
    diff ${VIVO_BASE}/vivo/myorg/my-org.el $HOME/.emacs.d/my-org.el
}

case "$1" in
    emacs)
	chk_cfg_emacs
	;;
    *)
	echo "Check my configurations"
	;;
esac
