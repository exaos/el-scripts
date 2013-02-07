#!/usr/bin/env python
# -*- mode: python; coding: utf-8; -*-
import yaml, os, sys
import subprocess as sp

def get_cmd_path(cmd):
    if os.path.isfile(cmd): return os.path.abspath(cmd)
    output = sp.Popen(["which", cmd], stdout=sp.PIPE).communicate()[0]
    return os.path.abspath(output.strip())

vcs_tools = {
    "git": { "path": get_cmd_path("git"),
             "cmds": [
                 "pull origin",
                 "remote prune origin",
                 "gc --aggressive --prune=now"] },
    "git_svn": { "path": get_cmd_path("git"),
                 "cmds":["svn fetch", "svn rebase -l"] },
    "hg":  {"path": get_cmd_path("hg"),  "cmds":["pull", "update"] },
    "bzr": {"path": get_cmd_path("bzr"), "cmds":["pull",] },
    "svn": {"path": get_cmd_path("svn"), "cmds":["update",]},
    }

#--------- loop over repos ----------
def repo_up(base,p,vcs):
    pcwd = os.path.join(base,p)
    for c in vcs["cmds"]:
        print("\n==========================================")
        print("Path: %s\nExec: %s %s\n"%(pcwd,vcs["path"],c))
        prog = [vcs["path"],] ; prog.extend(c.split())
        ret = sp.Popen(prog, cwd=pcwd)
        ret.wait()
        if ret.returncode: return (False, [pcwd, vcs["path"], c])
    return (True,None)

def up_repos_dir(path):
    repos = yaml.load(open(os.path.join(path,"repos.yaml"),"r"))
    err_list = []
    for v in list(vcs_tools.keys()):
        if v not in repos or not repos[v]: continue
        vcs = { "path": vcs_tools[v]["path"], }
        if "cmds" in repos and v in repos["cmds"] \
                and len(repos["cmds"][v])>0:
            vcs["cmds"] = repos["cmds"][v]
        else:
            vcs["cmds"] = vcs_tools[v]["cmds"]
        for p in repos[v]:
            bret, err = repo_up(path, p, vcs)
            if not bret: err_list.append(err)
    return err_list

def print_errors(e_l):
    n_err = 0
    print("-----------------------------------")
    for i in range(len(e_l)):
        for j in range(len(e_l[i])):
            n_err = n_err + 1
            print("==> ERROR: No. %d"%(n_err))
            print("path: %s"%(e_l[i][j][0]))
            print("exec: %s %s\n"%(e_l[i][j][1],e_l[i][j][2]))
    print("\nTotal errors: %d"%(n_err))

if __name__=="__main__":
    if len(sys.argv)>1:
        elist = []
        for i in range(1,len(sys.argv)):
            el = up_repos_dir(sys.argv[i])
            if len(el)>0: elist.append(el)
        print_errors(elist)
    else:
        print("Usage: repos-up [path1] [path2] [...]")

