#!/bin/bash

LOG_DIR=/var/log/mod_evasive/

IP_LIST=`ls -1 ${LOG_DIR} | awk -F'-' '{ print $2 }' | sort -n`

for i in ${IP_LIST} ; do
    j=`cat ${LOG_DIR}/dos-$i`
    # echo -e "$i   \t $j"
    printf "%-15s  %d\n" $i $j
done > dos-ip-list.txt
