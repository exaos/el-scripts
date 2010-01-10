#!/bin/sh
# Copyright (c) 2007 Cisco Systems, Inc.  All rights reserved.
#
# File installed for Bourne-shell startups to select which MPI
# installation to use.  Not using "alternatives" because we want to be
# able to set per-user level defaults, not just system-wide defaults.

mpi_selector_dir="/var/lib/mpi-selector/data"
mpi_selector_homefile="$HOME/.mpi-selector"
mpi_selector_sysfile="/etc/sysconfig/mpi-selector"

mpi_selection=
if test -f "$mpi_selector_homefile"; then
    mpi_selection=`cat $mpi_selector_homefile`
elif test -f "$mpi_selector_sysfile"; then
    mpi_selection=`cat $mpi_selector_sysfile`
fi

if test "$mpi_selection" != "" -a -f "$mpi_selector_dir/$mpi_selection.sh"; then
    . "$mpi_selector_dir/$mpi_selection.sh"
fi
