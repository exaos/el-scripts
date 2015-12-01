#!/bin/bash
# -*- mode: shell-script; coding: utf-8; -*-
# by Exaos Lee (exaos.lee@gmail.com)

usage() {
    echo "Usage: $0 [opts] <ver>"
    echo "Options:"
    echo "  -b|--base <dir>       -- geant4 basedir"
    echo "  -c|--cxx <g++|icpc>   -- setup C++ compiler"
    echo "  -d|--data <dir>       -- data basedir"
    echo "  -w|--work <dir>       -- geant4 workdir"
    echo "  -t|--term <terminal>  -- terminal to run geant4"
    echo "  -s|--shell <shell>    -- shell to run geant4"
    echo "  -h|--help             -- show this help"
}

while [ x"$1" != x ]
do
    case "$1" in
        -b|--base)
            shift 1
            G4BASEDIR=$1
            ;;
        -c|--cxx)
            shift 1
            G4CXX=$1
            ;;
        -d|--data)
            shift 1
            G4DATA=$1
            ;;
        -w|--work)
            shift 1
            G4WORKDIR=$1
            ;;
        -t|--term)
            shift 1
            G4TERMCMD=$1
            ;;
        -s|--shell)
            shift 1
            G4SHELLCMD=$1
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            G4VERSION=$1
            ;;
    esac
    shift 1
done

export G4BASEDIR=${G4BASEDIR:-/Bogo/Programs/Geant4}
export G4WORKDIR=${G4WORKDIR:-$HOME/Utils/GEANT4}
export G4DATA=${G4BASEDIR}/Data
export G4CXX=${G4CXX:-g++}
export G4VERSION=${G4VERSION:-9.6.p04}
export G4INSTALL=${G4BASEDIR}/${G4VERSION}-${G4CXX}
export G4SOURCEDIR=${G4BASEDIR}/Sources/geant4.${G4VERSION}

# Setup geant4 generated script
OLDPATH=`pwd`
cd $G4INSTALL/bin/
source ./geant4.sh
cd $OLDPATH

G4TERMCMD=${G4TERMCMD:-xterm}
G4SHELLCMD=${G4SHELLCMD:-$SHELL}
${G4TERMCMD} -e "${G4SHELLCMD}"

