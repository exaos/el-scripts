#!/bin/bash

## check ROOT privilege
if [[ $EUID -ne 0 ]]; then
    echo "**ERROR** This script should be run using sudo or as the root user"
    exit 1
fi

## 

LOG_DIR=/var/log/mod_evasive/
IP_LIST=`ls -1 ${LOG_DIR} | awk -F'-' '{ print $2 }' | sort -n`
UFW_DENY_LIST=`ufw status | grep "Anywhere" | grep "/tcp"`

function is_ip_in_ufw()
{
    is_in=`echo ${UFW_DENY_LIST} | grep "$1/tcp"`
    if [[ X"${is_in}" == X ]]; then
	echo "no"
    else
	echo "yes"
    fi
}

function add_ip_to_ufw()
{
    if [[ `is_ip_in_ufw $1` == "no" ]]; then
	echo "adding $1 to ufw deny list ..."
	ufw insert 10 deny proto tcp from $1
    else
	echo "$1 already added"
    fi
}

for ip in ${IP_LIST} ; do
    add_ip_to_ufw ${ip}
done
