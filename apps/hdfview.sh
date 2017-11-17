#!/bin/bash

# Set up default variable values if not supplied by the user.
# This script file is used to execute the hdfview utility
# ... hdfview.root property is for the install location
# ...... default location is system property user.dir
# ... hdfview.workdir property is for the working location to find files
# ...... default location is system property user.home
#

#HDFVIEW_PATH=$HOME/Utils/HDFView-3.0.0
#export JAVABIN=${HDFVIEW_PATH}/jre/bin
#JAVABIN=/usr/lib/jvm/jdk-8-oracle-x64/bin
#export INSTALLDIR=${HDFVIEW_PATH}

#$JAVABIN/java $JAVAOPTS -Xmx1024M -Djava.library.path="$INSTALLDIR/lib" -Dhdfview.root="$INSTALLDIR" -jar "$INSTALLDIR/lib/HDFView.jar" $*

# alternate invocation when using modules
#$JAVABIN/java $JAVAOPTS -Xmx1024M -Djava.library.path="$INSTALLDIR/lib:$INSTALLDIR/lib/ext" -Dhdfview.root="$INSTALLDIR" -cp "$INSTALLDIR/lib/jarhdf-3.99.0.jar:$INSTALLDIR/lib/jarhdf5-3.99.0.jar:$INSTALLDIR/lib/slf4j-nop-1.7.5.jar:$INSTALLDIR/lib/HDFView.jar" hdf.view.HDFView $*

HV_PATH=$(dirname $(readlink -f $0))
JAVA_EXE=$(which java)
JAVAOPTS="-Xmx1024M"

#${JAVA_EXE} $JAVAOPTS -Xmx1024M \
#-Djava.library.path="${HV_PATH}/lib" \
#-Dhdfview.root="${HV_PATH}" \
#-cp "${HV_PATH}/lib/jarhdf-4.2.12.jar:${HV_PATH}/lib/jarhdf5-1.10.1.jar:${HV_PATH}/lib/slf4j-simple.1.7.5.jar:${HV_PATH}/lib/slf4j-api.1.7.5.jar:${HV_PATH}/lib/HDFView.jar" \
#hdf.view.HDFView "$@"

${JAVA_EXE} ${JAVAOPTS} \
-Djava.library.path="${HV_PATH}/lib" \
-Dhdfview.root="${HV_PATH}" \
-cp "${HV_PATH}/lib/*" \
hdf.view.HDFView "$@"

