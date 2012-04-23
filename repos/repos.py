#!/usr/bin/env python
'''Purpose: apply often-used commands to your repositories as defined

Usage: %s [options] <commands> [cmd-options] [id] [...]

Options:
  -c | --config <filename>  -- specify configuration file
  -h | --help               -- show usage
  -V | --verbose            -- verbose output
  -v | --version            -- show version

Commands:
  ls | list   -- show objects specified or all if no one given
  st | status -- show group or repository status (default if no cmds)
  info        -- show group or repository information
  cmds        -- command sequence defined in configure file (default)
  sync        -- syncronize (pull and push) with repository defined

  others: fetch, pull, push

ID:
  -a | --all     -- all repositories defined
  [repo | group] -- repository or group ID
'''

import os,sys
import subprocess as sp
try:
    from argparse import ArgumentParser
except:
    printf("Error: you'd better install module argparse or python >= 2.7")
    exit(1)
try:
    import yaml
except:
    printf("Error: no yaml module found!")
    exit(1)

#-----------------------------------------------------------
# common utilities

def which(program):
    """Return program's absolute path."""
    is_exe = lambda f: os.path.exists(f) and os.access(f,os.X_OK)
    fp, fn = os.path.split(program)
    if fp and is_exe(program): return program
    f_list = filter(is_exe,
                    [ os.path.join(p,fn) for p in
                      os.environ["PATH"].split(os.pathsep) ])
    if f_list: return f_list[0]
    return None

def set_dict_default(ddst, dsrc):
    '''assign default values to dict.'''
    if type(ddst) != dict or type(dsrc) != dict: return
    for k in list(dsrc):
        if k not in ddst: ddst[k] = dsrc[k]
        else:
            if type(ddst[k]) == dict:
                if type(dsrc[k]) == dict: assign_dict_default(ddst[k], dsrc[k])
            else:
                if not ddst[k]: ddst[k] = dsrc[k]

#-----------------------------------------------------------
# command line options

msg_ret = {
    0  : "Successful",
    -1 : "Configure file not found",
    -2 : "Invalid configure file",
    -3 : "Invalid global options",
    -4 : "Invalid group options",
    -5 : "Invalid repository options",
    -6 : "VCS tool not available",
    }

g_fcfg = ""
g_cmds = []
g_objs = []
g_verb = False
g_cmds_av = [ "list", "status", "info", "cmds", "sync", "fetch", "pull", "push"]

def cli_options(argv):
    global g_fcfg, g_cmds, g_objs, g_verb
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
# parsing configure file and assign missing properties to defaults

cfg_groups = { "orphan":{ 'id': 'orphan', "type": "group", "units": []}, }
cfg_repos  = {}
cfg_global = {}

def cfg_set_default_global():
    '''Assign default global values.'''
    global cfg_global
    set_dict_default(
        cfg_global,
        { 'vcs': 'git',
          'path': os.path.join(os.environ['HOME'],'Workspace'),
          'git-svn': { 'path': which('git'),
                       'cmds': ["svn fetch", "svn rebase -l", "gc --aggressive"] },
          'git': { 'path': which('git'),
                   'cmds': [ "fetch --all", "pull origin", "gc --aggressive" ] },
          'hg':  { 'path': which('hg'),
                   'cmds': [ "pull", "merge" ] },
          'bzr': { 'path': which('bzr'),
                   'cmds': [ "pull", ] },
          'svn': { 'path': which('svn'),
                   'cmds': [ "update", ] },
          'cvs': { 'path': which('cvs'),
                   'cmds': [] },
          'id': 'global' } )
    # check availability of VCS tools, remove un-available tools
    av_keys = cg_keys = list(cfg_global.keys())
    for k in ['vcs', 'path', 'desc']:
        if k in cg_keys: cg_keys.remove(k)
    for v in cg_keys:
        if type(cfg_global[v]) != dict or not which(cfg_global[v]['path']):
            cfg_global.pop(v)
            av_keys.remove(v)

    # No VCS available!
    if not av_keys: return -3

    return 0

def get_by_id_path(id_d):
    global cfg_global, cfg_groups, cfg_repos

    if id_d == 'global': return os.path.abspath(cfg_global['path'])

    dic_d = cfg_repos[id_d] if id_d in cfg_repos else cfg_groups[id_d]
    # abosulte path
    if "path" in dic_d and os.path.isabs(dic_d['path']): return dic_d['path']

    # relative path
    ppath = get_by_id_path(dic_d['parent'])
    if "path" not in dic_d or not dic_d["path"]:
        return os.path.join(ppath, id_d)

    return os.path.join(ppath, dic_d['path'])

def get_by_id_vcs (id_d):
    global cfg_global, cfg_groups, cfg_repos
    if id_d == 'global': return cfg_global['vcs']

    dic_d = cfg_repos[id_d] if id_d in cfg_repos else cfg_groups[id_d]
    if 'vcs' not in dic_d or not dic_d['vcs']:
        return get_by_id_vcs(dic_d['parent'])

    return dic_d['vcs']

def get_by_id_cmds(id_d, v):
    global cfg_global, cfg_groups, cfg_repos
    if id_d == 'global': return cfg_global[v]['cmds']

    dic_d = cfg_repos[id_d] if id_d in cfg_repos else cfg_groups[id_d]
    if 'cmds' not in dic_d or not dic_d['cmds']:
        return get_by_id_cmds(dic_d['parent'], v)

    return dic_d['cmds']

def cfg_set_default_id(id_d):
    global cfg_groups, cfg_repos
    if id_d == 'global': return

    dic_d = cfg_repos[id_d] if id_d in cfg_repos else cfg_groups[id_d]
    # parent
    if 'parent' not in dic_d or not dic_d['parent']:
        if not dic_d['parents'] or not dic_d['parents']:
            dic_d['parent'] = 'global'
        else:
            dic_d['parent'] = dic_d['parents'][0]
    # path
    dic_d["path"] = get_by_id_path(id_d)
    # vcs
    dic_d['vcs' ] = get_by_id_vcs( id_d)
    # cmds
    dic_d['cmds'] = get_by_id_cmds(id_d, dic_d['vcs'])

def cfg_set_defaults_group(gr):
    cfg_set_default_id(gr['id'])

def cfg_set_defaults_repo(repo):
    cfg_set_default_id(repo['id'])

def config_read():
    global cfg_groups, cfg_repos, cfg_global

    # load YAML
    try: cfg_tmp = yaml.load(open(g_fcfg))
    except: return -2

    # global settings
    cfg_global = cfg_tmp.pop("global")
    ret = cfg_set_default_global()
    if ret < 0: return ret

    # find groups and repos
    for k in list(cfg_tmp.keys()):
        if 'type' in cfg_tmp[k] and cfg_tmp[k]['type'] == 'group':
            cfg_groups[k] = cfg_tmp.pop(k)
            cfg_groups[k]['id'] = k
        else:
            cfg_repos[k] = cfg_tmp.pop(k)
            cfg_repos[k]['id'] = k
            cfg_repos[k]['type'] = 'repo'

    # Assign parents property to ids
    for k in list(cfg_groups.keys()):
        for r in cfg_groups[k]["units"]:
            if r not in cfg_repos.keys():
                cfg_repos[r] = { 'id': r, 'type': 'repo' }
            if "parents" not in cfg_repos[r].keys():
                cfg_repos[r]["parents"] = []
            cfg_repos[r]["parents"].append(k)

    # Find orphan repos ?
    for r in list(cfg_repos.keys()):
        if "parents" not in cfg_repos[r].keys() or not cfg_repos[r]["parents"]:
            cfg_repos[r]["parent"]  = "global"
            cfg_repos[r]["parents"] = ["orphan",]
            cfg_groups["orphan"]["units"].append(r)

    return 0

def print_test():
    # print
    from pprint import pprint
    pprint(cfg_global)
    for k in list(cfg_groups.keys()):
        print("Group [%s]:"%k)
        pprint(cfg_groups[k]["units"])
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
        print("Error: %s"%msg_ret[n_err])

#-----------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv)

