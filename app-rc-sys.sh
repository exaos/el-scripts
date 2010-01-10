#!/bin/sh
# Copyright (c) 2007 Exaos Lee, CNDL
#
# System-wide app_rc.sh for app-envsel
# Purpose: To provide the startup environment for app-envsel

APPENV_DATA=/var/lib/app-envsel/data
APPENV_SETDIR_SYS=/var/lib/app-envsel/env
APPENV_SETDIR_USER=$HOME/.config/app-envsel/env

if [ ! -d ${APPENV_DATA} ]; then
    echo "Data directory is not set for \"app-envsel\""
    exit 0
fi

## Read env selections from directory
[ -d ${APPENV_SETDIR_SYS} ]  && app_env_sys=$(ls -A ${APPENV_SETDIR_SYS})
[ -d ${APPENV_SETDIR_USER} ] && app_env_user=$(ls -A ${APPENV_SETDIR_USER})

if [ "${app_env_user}" ]; then
    for env in ${app_env_user} ; do
	[ -f ${APPENV_DATA}/${env}.sh ] && . ${APPENV_DATA}/${env}.sh
    done
elif [ "${app_env_sys}" ]; then
    for env in ${app_env_sys} ; do
	[ -f ${APPENV_DATA}/${env}.sh ] && . ${APPENV_DATA}/${env}.sh
    done
fi
