#!/bin/sh
# Copyright (c) 2007 Exaos Lee, CNDL
#
# User-wide app_rc.sh for app-envsel
# Purpose: To provide the startup environment for app-envsel

APPENV_DATA_SYS=/var/lib/app-envsel/data
APPENV_DATA_USER=$HOME/.config/app-envsel/data
APPENV_SETDIR_USER=$HOME/.config/app-envsel/env


[ -d ${APPENV_DATA_SYS} ] && APPENV_DATA=${APPENV_DATA_SYS}
APPENV_DATA=${APPENV_DATA:-${APPENV_DATA_USER}}
if [ ! -d ${APPENV_DATA} ]; then
    echo "Data directory is not set for \"app-envsel\""
else
    ## Read env selections from directory
    [ -d ${APPENV_SETDIR_USER} ] && app_env_user=$(ls -A ${APPENV_SETDIR_USER})
    if [ "${app_env_user}" ]; then
	for env in ${app_env_user} ; do
	    echo "Applying app environment: $env ..."
	    [ -f ${APPENV_DATA}/${env}.sh ] && . ${APPENV_DATA}/${env}.sh
	done
    fi
fi

