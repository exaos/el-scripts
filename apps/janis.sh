#!/bin/sh
JANISPATH=$(dirname $(readlink -f $0))/4.0

cd ${JANISPATH}

# java -Djdbc.drivers=org.h2.Driver,com.mckoi.JDBCDriver -Xms100M -Xmx256M \
# -jar Janis.jar
# -Dlog4j.configuration=file:./log4j.properties 
# cd ..

java -Xms100M -Xmx512M -jar Janis.jar

