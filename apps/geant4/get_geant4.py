#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Exaos
'''

import os
import os.path as path
import yaml
import subprocess as sp
from pprint import pprint


def fetch_file(url, fn, cwd='.'):
    fetcher = ["wget", "-c"]
    fetcher.extend(["-O", fn, url])
    ret = sp.Popen(fetcher, cwd=cwd)
    ret.wait()
    if ret.returncode: return False
    return True


usage = """Usage: %s [command] [geant4-version]

commands:
   list           -- list versions
   get [ver]      -- fetch geant4 source of version [ver]
   get-data [ver] -- fetch data needed by version [ver]
"""

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(usage % (sys.argv[0]))
        exit(0)

    g4vers = yaml.load(open("versions.yaml"))
    comm = g4vers.pop("common")

    if sys.argv[1] == 'list':
        pprint(g4vers.keys())
    elif sys.argv[1] == 'get' and len(sys.argv) > 2:
        for v in sys.argv[2:]:
            if v not in g4vers: continue
            fmt = g4vers[v]['format'] if 'format' in g4vers[v] else 'tar.gz'
            fn = "geant4.%s.%s" % (v, fmt)
            url = "%s/%s" % (comm['base_url'], fn)
            print url, fn
            fetch_file(url, fn, cwd=os.getcwd())
    elif sys.argv[1] == 'get-data' and len(sys.argv) > 2:
        for v in sys.argv[2:]:
            for k in g4vers[v]['data']:
                fn = "%s.%s.tar.gz" % (k, str(g4vers[v]['data'][k]))
                url = "%s/%s" % (comm['base_url'], fn)
                fetch_file(url, fn, cwd=os.getcwd())
    else:
        print(usage % (sys.argv[0]))
