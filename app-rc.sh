#!/bin/bash
# Copyright (c) 2007 Exaos Lee, CNDL
#
# System-wide app_rc.sh for app-envsel
# Purpose: To provide the startup environment for app-envsel

AE_DATA_SYS=/var/lib/app-envsel/data
AE_SETD_SYS=/var/lib/app-envsel/env
AE_DATA_USER=$HOME/.config/app-envsel/data
AE_SETD_USER=$HOME/.config/app-envsel/env

[ -d ${AE_DATA_SYS} ] && AE_DATA=${AE_DATA_SYS}
[ -z "${AE_DATA}"   ] && AE_DATA=${AE_DATA_USER}
echo ${AE_DATA}

set_env()
{
    appn=$1
    [ -f ${AE_SETD_USER}/$appn ] && appv=$(cat ${AE_SETD_USER}/$appn)
    if [ -z "$appv" ] && [ -f ${AE_SETD_SYS}/$appn ]; then
	appv=$(cat ${AE_SETD_SYS}/$appn)
    fi
    echo -n "Setting $appn: ${AE_DATA}/${appn}_$appv.sh ... "
    if [ -f ${AE_DATA}/${appv}.sh ]; then
	. ${AE_DATA}/${appn}_${appv}.sh
	echo "DONE!"
    else
	echo "FAILED"
    fi
    unset appv
    unset app
}

if [ ! -d ${AE_DATA} ]; then
    echo "Data directory is not set for \"app-envsel\""
else
    [ -d ${AE_SETD_SYS} ]  && app_env_sys=$(ls -A ${AE_SETD_SYS})
    [ -d ${AE_SETD_USER} ] && app_env_user=$(ls -A ${AE_SETD_USER})

    app_list=(`echo ${app_env_user} ${app_env_sys} | tr " " "\n" | sort -u `)
    if [ ${#app_list} -gt 0 ]; then
	for app in ${app_list} ; do set_env $app; done
	unset app
    fi
    unset app_list
fi

unset AE_DATA

