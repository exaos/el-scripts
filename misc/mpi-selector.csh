#!/bin/csh
# Copyright (c) 2007 Cisco Systems, Inc.  All rights reserved.
#
# File installed for Bourne-shell startups to select which ICC
# installation to use.  Not using "alternatives" because we want to be
# able to set per-user level defaults, not just system-wide defaults.

set icc_selector_dir="/var/lib/icc-selector/data"
set icc_selector_homefile="$HOME/.icc-selector"
set icc_selector_sysfile="/etc/sysconfig/icc-selector"

set icc_selection=
if (-f "$icc_selector_homefile") then
    set icc_selection=`cat $icc_selector_homefile`
else if (-f "$icc_selector_sysfile") then
    set icc_selection=`cat $icc_selector_sysfile`
endif

if ("$icc_selection" != "" && -f "$icc_selector_dir/$icc_selection.csh") then
    source "$icc_selector_dir/$icc_selection.csh"
endif
