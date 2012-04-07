#!/usr/bin/env python
'''
Usage: %s [options] <commands> [cmd-options] [object]

Purpose: apply often-used commands to your repositories as defined

Options:

  -c | --config <filename>  -- specify configuration file

  If not given, it will use the found one of ./repos.yaml,
  ~/Workspace/repos.yaml and ~/.config/repos.yaml

  -h | --help               -- show usage
  -V | --verbose            -- verbose output
  -v | --version            -- show version

Commands:

  ls | list    -- show objects specified or all if no one given
  st | status  -- show repository status
  info         -- show repository information
  fetch        -- fetch remotes
  pull         -- fetch and update changes from upstreams
  push         -- push changes to upstream branches
  sync         -- syncronize (pull and push)  with repository defined
  de | defined -- command sequence defined in configure file (default)

  If command sequence is not defined in configure file, default command
  will be "status".

Object:

  -a | --all   -- all repositories defined
  [repo]       -- repository id
  [group]      -- group id

  Multi objects are accepted.
'''

import os,sys
import yaml
import subprocess as sp

#-----------------------------------------------------------
# command line options

errmsg_cfg = { 0  : "successful",
               -1 : "Configure file not found",
               -2 : "Invalid configure file",
               -3 : "Invalid global options",
               -4 : "Invalid group options",
               -5 : "Invalid repository options" }

g_fcfg = ""
g_cmds = []
g_objs = []
g_verb = False
g_cmds_list = [ "list", "status", "info", "fetch", "pull", "push", "sync", "defined" ]

def cli_options(argv):
    global g_fcfg, g_cmds, g_objs, g_verb
    from argparse import ArgumentParser
    ok_opt = True
    parser = ArgumentParser()

    # help, verbose, version

    # parse commands

    # find configure file
    dir_home = os.getenv("HOME")
    f_list = [ "repos.yaml",
               os.path.join(dir_home, "Workspace/repos.yaml"),
               os.path.join(dir_home, ".config/repos.yaml") ]
    fc_tmp = list(filter(os.path.isfile, f_list))
    if not fc_tmp: return -1
    g_fcfg = fc_tmp[0]

    return 0

#-----------------------------------------------------------
# parsing configure file
cfg_groups = { "orphan":{ "type": "group", "repos": []} }
cfg_repos  = {}
cfg_global = {}

def config_read():
    global cfg_groups, cfg_repos, cfg_global

    # load YAML
    try: cfg_tmp = yaml.load(open(g_fcfg))
    except: return -2

    # global settings
    cfg_global = cfg_tmp.pop("global")
    if not cfg_global: return -3

    # find groups
    for k in list(cfg_tmp.keys()):
        if 'type' in cfg_tmp[k] and cfg_tmp[k]['type'] == 'group':
            cfg_groups[k] = cfg_tmp.pop(k)
        else:
            cfg_repos[k] = cfg_tmp.pop(k)

    # Assign group property to repos
    for k in list(cfg_groups.keys()):
        for r in cfg_groups[k]["repos"]:
            if r not in cfg_repos.keys():
                cfg_repos[r] = {}
            if "groups" not in cfg_repos[r].keys():
                cfg_repos[r]["groups"] = []
            cfg_repos[r]["groups"].append(k)

    # Find orphan repos
    for r in list(cfg_repos.keys()):
        if "groups" not in cfg_repos[r].keys() or not cfg_repos[r]["groups"]:
            cfg_repos[r]["groups"] = ["orphan",]
            cfg_groups["orphan"]["repos"].append(r)

    return 0

def config_fill():
    pass

def print_test():
    # print
    from pprint import pprint
    pprint(cfg_global)
    for k in list(cfg_groups.keys()):
        print("Group [%s]:"%k)
        pprint(cfg_groups[k]["repos"])
    pprint(cfg_groups.keys())
    pprint(cfg_repos.keys())

#-----------------------------------------------------------
# Main
def main(argv):
    if len(argv) < 2 or cli_options(argv) != 0:
        print(__doc__ % sys.argv[0])
        exit(0)
    n_err = config_read()
    if n_err == 0:
        config_fill()
        print_test()
    else:
        print(g_fcfg)
        print("Error: %s"%errmsg_cfg[n_err])

#-----------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv)

