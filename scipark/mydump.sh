#!/bin/bash

DB_BAK_DIR=/srv/archives/db-backup
DB_LIST=(scipark scitoday)
FN_DATE=`date '+%Y%m%dT%H%M'`

for i in "${DB_LIST[@]}" ; do
    # echo ${DB_BAK_DIR}/${i}_${FN_DATE}.sql.gz
    mysqldump ${i} | gzip > ${DB_BAK_DIR}/${i}_${FN_DATE}.sql.gz
done
