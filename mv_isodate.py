#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Move file into directory like yyyy/mm/dd.
@Exaos
'''

import os,sys,re,shutil
import os.path as path

def isodate_extract(fn):
    yyyy,mm,dd = None, None, None
    sm = re.search("\d{4}-\d{2}-\d{2}",fn)
    if sm == None:
        sm = re.search("\d{8}",fn)
        if sm == None: return None,None,None
        pdate = sm.group(0)
        yyyy,mm,dd = pdate[0:4], pdate[4:6], pdate[6:8]
    else:
        pdate = sm.group(0)
        yyyy,mm,dd = pdate[0:4], pdate[5:7], pdate[8:10]
    if int(yyyy) < 1900 or int(yyyy)>2100 or \
       int(mm)<1 or int(mm)>12 or int(dd) <1 or int(dd)>31:
           return None,None,None
    return yyyy,mm,dd

def isodate_mv(fn, basedir="."):
    if not path.isfile(fn): return
    yyyy,mm,dd = isodate_extract(fn)
    if not (yyyy and mm and dd): return
    isodir = path.join(basedir, yyyy, mm, dd)
    try:
        os.makedirs(isodir)
    except:
        pass
    # print(isodir)
    print("Moving "+fn+" to "+isodir+"...")
    shutil.move(fn,path.join(isodir,fn))
    
def main():
    pass

if __name__=="__main__":
    if len(sys.argv) > 1:
        for i in sys.argv[1:]:
            isodate_mv(i)
    else:
        print("usage: %s [file1] [file2] ..."%(sys.argv[0]))

