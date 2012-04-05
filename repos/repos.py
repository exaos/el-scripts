#!/usr/bin/env python
'''
Purpose: manage your repositories
Usage: %s [options] <commands> [cmd-options]

Default Configure: ~/Workspace/repos.yaml or ~/.config/repos.yaml

Global options:
  -c | --config <filename>  -- specify configuration file
  -h | --help               -- show usage
  -V | --verbose            -- verbose output

Commands:
  st | status   -- show repository status
  info          -- show repository information
  ci | commit   -- commit changes
  pull          -- fetch and update changes from upstream
  push          -- push changes to upstream branches
'''
import os,sys
import yaml
import subprocess as sp

# find configure file
dir_home = os.getenv("HOME")
f_config = list(
    filter( os.path.isfile,
            [ os.path.join(dir_home, "Workspace/repos.yaml"),
              os.path.join(dir_home, ".config/repos.yaml"),
              ] ))
if not f_config: sys.stderr.write("Configure file not found!\n"); exit(1)

############################################################
# parsing configure file
cfg_groups = {}
cfg_repos  = {}

try: cfg_tmp = yaml.load(open(f_config[0]))
except:
    sys.stderr.write("Invalid configure file!")
    exit(1)

# global settings
cfg_global = cfg_tmp.pop("global")
if not cfg_global: sys.stderr.write("Invalid global options"); exit(1)

# find groups
for k in list(cfg_tmp.keys()):
    if 'type' in cfg_tmp[k] and cfg_tmp[k]['type'] == 'group':
        cfg_groups[k] = cfg_tmp.pop(k)
    else:
        cfg_repos[k] = cfg_tmp.pop(k)

# format configurations
cfg_groups["orphan"] = { "type": "group", "repos": [] }

# Assign group property to repos
for k in list(cfg_groups.keys()):
    for r in cfg_groups[k]["repos"]:
        if r not in cfg_repos.keys(): cfg_repos[r] = {}
        if "groups" not in cfg_repos[r].keys(): cfg_repos[r]["groups"] = []
        cfg_repos[r]["groups"].append(k)

# Find orphan repos
for r in list(cfg_repos.keys()):
    if "groups" not in cfg_repos[r].keys() or not cfg_repos[r]["groups"]:
        cfg_repos[r]["groups"] = ["orphan",]
        cfg_groups["orphan"]["repos"].append(r)

# print
from pprint import pprint
pprint(cfg_global)
for k in list(cfg_groups.keys()):
    print("Group [%s]:"%k)
    pprint(cfg_groups[k]["repos"])
#pprint(cfg_groups.keys())
#pprint(cfg_repos.keys())

#-----------------------------------------------------------
# Main
if __name__ == "__main__":
    pass
    #print(__doc__ % sys.argv[0])

