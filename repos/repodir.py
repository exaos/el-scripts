#!/usr/bin/env python
# -*- mode: python; coding: utf-8; -*-
'''
Utility for manipulating a repository.
'''
import os
import sys
import subprocess as sp
import yaml


def get_cmd_path(cmd):
    if os.path.isfile(cmd):
        return os.path.abspath(cmd)
    output = sp.Popen(["which", cmd], stdout=sp.PIPE).communicate()[0]
    return str(os.path.abspath(output.strip()))


vcs_tools = {
    "git": get_cmd_path("git"),
    "git_svn": get_cmd_path("git") + " svn",
    "hg": get_cmd_path("hg"),
    "bzr": get_cmd_path("bzr"),
    "svn": get_cmd_path("svn"),
}

vcs_commands = {
    "pull": None,
    "fetch": None,
    "update": None,
    "info": None,
    "status": None,
    "diff": None,
    "log": None,
    "run": None
}

#--------- loop over repos ----------


def repo_up(base, repo, vcs):
    pcwd = os.path.join(base, repo)
    print("\n==========================================\nPath: {}\n".format(
        pcwd))
    for c in vcs["cmds"]:
        print("Exec: {0} {1} {2}\n".format(pcwd, vcs["path"], c))
        prog = [
            vcs["path"],
        ]
        prog.extend(c.split())
        ret = sp.Popen(prog, cwd=pcwd)
        ret.wait()
        if ret.returncode:
            return (False, [pcwd, vcs["path"], c])
    return (True, None)


def up_repos_dir(path):
    repos = yaml.load(open(os.path.join(path, "repos.yaml"), "r"))
    err_list = []
    for v in list(vcs_tools.keys()):
        if v not in repos or not repos[v]:
            continue
        vcs = {
            "path": vcs_tools[v]["path"],
        }
        if "cmds" in repos and v in repos["cmds"] and len(
                repos["cmds"][v]) > 0:
            vcs["cmds"] = repos["cmds"][v]
        else:
            vcs["cmds"] = vcs_tools[v]["cmds"]
        for p in repos[v]:
            bret, err = repo_up(path, p, vcs)
            if not bret:
                err_list.append(err)
    return err_list


def print_errors(e_l):
    n_err = 0
    print("-----------------------------------")
    for i in range(len(e_l)):
        for j in range(len(e_l[i])):
            n_err = n_err + 1
            print("==> ERROR: No. {}".format(n_err))
            print("path: {}".format(e_l[i][j][0]))
            print("exec: {} {}\n".format(e_l[i][j][1], e_l[i][j][2]))
    print("\nTotal errors: {}".format(n_err))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        elist = []
        for i in range(1, len(sys.argv)):
            el = up_repos_dir(sys.argv[i])
            if len(el) > 0:
                elist.append(el)
        print_errors(elist)
    else:
        print("Usage: repos-up [path1] [path2] [...]")
