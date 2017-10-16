#!/bin/bash

KMAXROOT=$(dirname $(readlink -f $0))
# Use sun-java6-jdk as default
#JAVA=/usr/lib/jvm/java-6-sun/bin/java
JAVA=java

if [[ ! -d $HOME/.kmax ]] ; then
	cp -rp ${KMAXROOT}/.kmax $HOME/
fi

cd ${KMAXROOT} && ${JAVA} -jar Kmax.jar "$@"
