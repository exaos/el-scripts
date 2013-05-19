#!/usr/bin/env python
#-*- encoding: utf-8

import shutil, os, sys

def dest_name(d_name):
    d_tmp = d_name.split('-')
    if d_tmp and d_tmp[0] != d_name:
        return os.path.join('.',*d_tmp)
    return None

names = os.listdir(ur'.')

for d in names:
    d_dest = dest_name(d)
    if d_dest: shutil.move(d, d_dest)

