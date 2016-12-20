#!/usr/bin/env python2

import os, sys

def get_u8fn_fixed(fn):
    newfn = []
    for i in fn.decode("utf-8"):
	if ord(i)>256: newfn.append(i.encode("utf-8"))
	else: newfn.append(chr(ord(i)))
    return "".join(newfn)

def fix_wrong_u8(dname, isRename=False):
    newf = get_u8fn_fixed(dname)
    print dname,
    if dname != newf:
        # print ":-->", newf
        if isRename: os.rename(dname, newf)
    else:
        print ": Filename is OK!"
    r_dn = dname
    if isRename and os.path.isdir(newf) :       r_dn = newf
    elif not isRename and os.path.isdir(dname): r_dn = dname
    else: return
    print "\n====> Recursive fix names in dir:", r_dn, "\n"
    for fname in os.listdir(r_dn):
        fix_wrong_u8(os.path.join(r_dn,fname), isRename)

if __name__=='__main__':
    if len(sys.argv)>=2:
        isRename = True if '-f' in sys.argv else False
        for fn in sys.argv[1:]: fix_wrong_u8(fn, isRename)
    else:
        print """Usage: %s [-f]  [file] [file] ..."""%sys.argv[0]

