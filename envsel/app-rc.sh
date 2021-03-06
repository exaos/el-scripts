#!/bin/bash
# Copyright (c) 2010 Exaos Lee <Exaos.Lee(at)gmail.com>, CNDL
#
# Purpose: To provide the startup environment for app-envsel

AE_DATA_SYS=/var/lib/app-envsel/data
AE_SETD_SYS=/var/lib/app-envsel/env
AE_DATA_USER=$HOME/.config/app-envsel/data
AE_SETD_USER=$HOME/.config/app-envsel/env

set_env()
{
    appn=$1
    if [ -f ${AE_SETD_USER}/$appn ]; then
	appv=$(sed /\#/d ${AE_SETD_USER}/$appn | sed -n 1p)
    fi
    if [ -z "$appv" ] && [ -f ${AE_SETD_SYS}/$appn ]; then
	appv=$(sed /\#/d ${AE_SETD_SYS}/$appn | sed -n 1p)
    fi
    [ $TERM != "dumb" ] && echo -n "Setting $appn: "
    if [ -f ${AE_DATA_USER}/${appn}_${appv}.sh ]; then
	[ $TERM != "dumb" ] && echo -n "${AE_DATA_USER}/${appn}_$appv.sh .. "
	. ${AE_DATA_USER}/${appn}_${appv}.sh
	[ $TERM != "dumb" ] && echo "[DONE]"
    elif [ -f ${AE_DATA_SYS}/${appn}_${appv}.sh ]; then
	[ $TERM != "dumb" ] && echo -n "${AE_DATA_SYS}/${appn}_$appv.sh .. "
	. ${AE_DATA_SYS}/${appn}_${appv}.sh
	[ $TERM != "dumb" ] && echo "DONE!"
    else
	[ $TERM != "dumb" ] && echo "[FAILED]"
    fi
    unset appn appv
}

if [ ! -d ${AE_DATA_SYS} -a ! -d ${AE_DATA_USER} ]; then
    [ $TERM != "dumb" ] && echo "WARNING: Data directory is not ready for \"app-envsel\"!"
else
    [ -d ${AE_SETD_SYS} ]  && app_env_sys=$(ls -A ${AE_SETD_SYS})
    [ -d ${AE_SETD_USER} ] && app_env_user=$(ls -A ${AE_SETD_USER})

    app_list=(`echo ${app_env_user} ${app_env_sys} | tr " " "\n" | sort -u `)
    if [ ${#app_list} -gt 0 ]; then
	for app in ${app_list[@]} ; do set_env $app; done
	unset app
    fi
    unset app_list
fi

unset AE_DATA AE_DATA_SYS AE_DATA_USER
unset AE_SETD_SYS AE_SETD_USER

