#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Name:    git-fix-svn-tags
Purpose: Change remote tags to local ones after "git svn clone --stdlayout".
Author:  Exaos Lee <exaos@ciae.ac.cn>
Date:    2010-12-19
'''

import os


def git_fix_svn_tags(gdir, force=False):
    print("Change to dir %s" % gdir)
    os.chdir(gdir)
    svn_tags = []
    for l in os.popen("git show-ref").readlines():
        head, tag = l.strip().split()
        if "remotes/tags" in tag:
            svn_tags.append([head, tag.split("/")[-1]])
    for t in svn_tags:
        if force: cmd = "git tag -f %s %s" % (t[1], t[0])
        else: cmd = "git tag %s %s" % (t[1], t[0])
        print("Add tag: %s\n   HEAD: %s  ... " % (t[1], t[0]), end=' ')
        if os.system(cmd) == 0: print("OK!")
        else: print("Oops!")


if __name__ == "__main__":
    import sys, os
    usage = "Usage: %s [-f] <path-under-git-control>" % os.path.basename(
        sys.argv[0])
    if len(sys.argv) < 2:
        print(usage)
        exit()
    dlist = sys.argv[1:]
    if "-f" in dlist:
        force = True
        dlist.remove("-f")
    else:
        force = False
    for d in dlist:
        git_fix_svn_tags(d, force)
