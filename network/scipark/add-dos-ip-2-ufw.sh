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

WHITE_IPS=( 42.96.174.78 )

function add_ip_to_ufw ()
{
    if [[ ( ${IP_LIST} =~ $1 ) && ( ! ${WHITE_IPS[@]} =~ $1 ) && ( ! ${UFW_DENY_LIST} =~ $1 ) ]]; then
	echo "adding $1 to ufw deny list ..."
	ufw insert 10 deny proto tcp from $1
    fi
}

for ip in ${IP_LIST} ; do
    add_ip_to_ufw ${ip}
done
