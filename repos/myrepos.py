#!/usr/bin/env python

import os, sys
if sys.hexversion > 0x03000000:
    print("Python3 not supported!")
    exit(1)

import git

#-----------------------------------------------------------
myrepos = {
    'myorg'   : 'Library/MyOrg',
    'myconfig': 'Library/MyConfig',
    'mynotes' : 'Library/MyNotes',
    'daily'   : 'Workspace/exaos/daily',
    'goagent' : 'Workspace/exaos/goagent',
    'scripts' : 'Workspace/exaos/scripts',
    'org-src' : 'Workspace/exaos/site/org-src',
    'site'    : 'Workspace/exaos/site'
    }

#-----------------------------------------------------------
# sync with remote
def sync_repo(path, rpath):
    repo = git.Repo(path)
    # pull branches from rpath
    print "\n[==",path,':',rpath,"==]\n"
    bnames = [h.name for h in repo.heads]
    print "Pulling ..."
    if bnames:
	for name in bnames:
 	    print "[:: %10s ==> %-10s"%(name,name),
	    try:
		msg = repo.git.pull(rpath, ':'.join([name,name]))
		print "... [OK]\n", msg
            except: print "... [!ERROR!]"
    # push all branches to rpath
    print '-------------------------------------------------'
    print "Pushing all branches to", rpath,
    try:
	msg = repo.git.push(rpath,all=True)
	print "... [OK]\n", msg
    except:  print "... [!ERROR!]"

#-----------------------------------------------------------
def get_wkd_id(id_r):
    wkdir = myrepos[id_r]
    # check working copy
    if not os.path.isabs(wkdir):
        wkdir = os.path.join(os.environ['HOME'],myrepos[id_r])
    return wkdir

def repo_sync_local(id_r, lpath='Repos'):
    # check local dir to be synced ..
    syncdir = lpath
    if not os.path.isabs(lpath):
        syncdir = os.path.join(os.environ['HOME'],lpath)
    # syncing
    sync_repo(get_wkd_id(id_r), os.path.join(syncdir,'%s.git'%(id_r)))

def repo_sync_host(id_r, host=None):
    if not host: return
    # check SSH url?
    rpath = "exaos@%s:Repos/%s.git"%(host, id_r)
    # syncing
    sync_repo(get_wkd_id(id_r), rpath)

def repo_cmd(id_r,cmd):
    repo = git.Repo(get_wkd_id(id_r))
    print "\nExecuting %s on %s ..."%(cmd, myrepos[id_r])
    print '---------------------------------------------'
    try:    print repo.git.__getattr__(cmd)()
    except: print '[FAILED]'

#-----------------------------------------------------------
# handle all...
def repos_sync_local(lpath='Repos'):
    for id_r in list(myrepos): repo_sync_local(id_r, lpath)

def repos_sync_host(host=None):
    for id_r in list(myrepos): repo_sync_host(id_r, host)

def repos_cmd(cmd):
    for id_r in list(myrepos): repo_cmd(id_r, cmd)

#-----------------------------------------------------------
# Main
if __name__ == "__main__":
    usage = '''Usage: %s <cmd> [parameters]
Commands:
   + local|l <path>  --- Sync with local bare repositories
   + host|h  <host>  --- Sync with repos on [exaos@]host
   + <cmd>           --- Simple git commands, like 'gc', 'status', 'branch'
'''%sys.argv[0]
    bad_opt = False
    if len(sys.argv) < 2: bad_opt = True
    elif sys.argv[1] == 'l' or sys.argv[1] == 'local':
        lpath = 'Repos'
        if len(sys.argv) > 2: lpath = sys.argv[2]
        repos_sync_local(lpath)
    elif sys.argv[1] == 'h' or sys.argv[1] == 'host':
        if len(sys.argv) < 3: bad_opt = True
        else: repos_sync_host(sys.argv[2])
    else:
        repos_cmd(sys.argv[1])
    if bad_opt: print usage

