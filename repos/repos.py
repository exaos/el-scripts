#!/usr/bin/env python
'''Purpose: apply often-used commands to your repositories as defined

Usage: %s [options] <commands> [cmd-options] [obj] [obj ...]

Options:
  -c | --config <filename>  -- specify configuration file
  -h | --help               -- show usage
  -V | --verbose            -- verbose output
  -v | --version            -- show version

Commands:
  list    --  show objects specified or all if no one given
  status  --  show group or repository status (default if no cmds)
  info    --  show group or repository information
  cmds    --  command sequence defined in configure file (default)
  sync    --  syncronize (pull and push) with repository defined

  others: fetch, pull, push

Object:
  -a | --all  --  all repositories defined
  [obj]       --  repository or group ID
'''

import os, sys
import subprocess as sp
from pprint import pformat

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
    for f in [os.path.join(p,fn) for p in os.environ["PATH"].split(os.pathsep)]:
        if is_exe(f): return f
    return None

def set_dict_default(ddst, dsrc):
    '''assign default values to dict.'''
    if type(ddst) != dict or type(dsrc) != dict: return
    for k in list(dsrc):
        if k not in ddst: ddst[k] = dsrc[k]
        else:
            if type(ddst[k]) == dict:
                if type(dsrc[k]) == dict: set_dict_default(ddst[k], dsrc[k])
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
g_cmd  = []
g_objs = []
g_obj_all = False
g_verb = False
g_cmds_av = [ "list", "status", "info", "cmds", "sync", "fetch", "pull", "push"]

def cli_options(argv):
    global g_fcfg, g_cmd, g_objs, g_obj_all, g_verb

    par = ArgumentParser()
    par = ArgumentParser(prog="repos", description="Manage your repositories using YAML config")
    par.add_argument("-c", "--config", nargs=1, help="Override the default configure file")
    par.add_argument('-V', '--verbose', action='store_true')
    par_cmd = par.add_argument_group('command')
    par_cmd.add_argument('cmd', nargs=1, choices=g_cmds_av, default='status')
    par_cmd.add_argument('-a', '--all', action='store_true')
    par_cmd.add_argument('obj', nargs='*', help="objects to manage")
    pp = par.parse_args(argv)

    # find configure file
    dir_home = os.getenv("HOME")
    f_list = [ "repos.yaml",
               os.path.join(dir_home, "Workspace/repos.yaml"),
               os.path.join(dir_home, ".config/repos.yaml") ]
    if pp.config: f_list.insert(0, pp.config[0])
    fc_tmp = list(filter(os.path.isfile, f_list))
    if not fc_tmp: return -1
    g_fcfg = fc_tmp[0]

    # verbose
    g_verb = pp.verbose

    # command and objs
    g_cmd, g_objs, g_obj_all = pp.cmd[0], pp.obj, pp.all

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
        { 'type': 'global',
          'vcs': 'git',
          'path': os.path.join(os.environ['HOME'],'Workspace'),
          'git-svn': { 'path': which('git'),
                       'cmds': ["svn fetch", "svn rebase -l", "gc --aggressive"] },
          'git': { 'path': which('git'),
                   'cmds': [ "fetch --all", "pull", "gc --aggressive" ] },
          'hg':  { 'path': which('hg'),
                   'cmds': [ "pull", "merge" ] },
          'bzr': { 'path': which('bzr'),
                   'cmds': [ "pull", ] },
          'svn': { 'path': which('svn'),
                   'cmds': [ "update", ] },
          'cvs': { 'path': which('cvs'),
                   'cmds': [], },
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

def get_by_id_ptree(key):
    if key == 'global': return ""
    dic = get_by_id_dic(key)
    if not dic: return ""
    return get_by_id_ptree(dic['parent'])+'/'+key
def get_by_id_dic(key):
    global cfg_global, cfg_groups, cfg_repos
    if key == 'global': return cfg_global
    if key in cfg_groups: return cfg_groups[key]
    elif key in cfg_repos: return cfg_repos[key]
    else: return None

def get_by_id_path(key):
    global cfg_global, cfg_groups, cfg_repos

    if key == 'global': return os.path.abspath(cfg_global['path'])

    dic = get_by_id_dic(key)
    if not dic: return None

    # abosulte path
    if "path" in dic and os.path.isabs(dic['path']): return dic['path']

    # relative path
    pp = get_by_id_path(dic['parent'])
    if "path" not in dic or not dic["path"]: return os.path.join(pp, key)

    return os.path.join(pp, dic['path'])
def get_by_id_vcs (key):
    global cfg_global, cfg_groups, cfg_repos
    if key == 'global': return cfg_global['vcs']

    dic = get_by_id_dic(key)
    if 'vcs' not in dic or not dic['vcs']:
        return get_by_id_vcs(dic['parent'])

    return dic['vcs']

def get_by_id_cmds(key, v):
    global cfg_global, cfg_groups, cfg_repos
    if key == 'global': return cfg_global[v]['cmds']

    dic = get_by_id_dic(key)
    if 'cmds' not in dic or not dic['cmds']:
        return get_by_id_cmds(dic['parent'], v)

    return dic['cmds']

def cfg_set_default_id(key):
    global cfg_groups, cfg_repos
    if key == 'global': return

    dic = get_by_id_dic(key)
    # path
    dic["path"] = get_by_id_path(key)
    # vcs
    dic['vcs' ] = get_by_id_vcs (key)
    # cmds
    dic['cmds'] = get_by_id_cmds(key, dic['vcs'])
    # desc
    if 'desc' not in dic: dic['desc'] = 'Not given'

def config_reader():
    """Read configuration from YAML file."""
    global cfg_groups, cfg_repos, cfg_global

    # load YAML
    try: cfg_tmp = yaml.load(open(g_fcfg))
    except: return -2

    # global settings
    if 'global' in cfg_tmp: cfg_global = cfg_tmp.pop("global")
    ret = cfg_set_default_global()
    if ret < 0: return ret

    # find groups and repos
    for k in list(cfg_tmp.keys()):
        dic = dict()
        if ('type' in cfg_tmp[k] and cfg_tmp[k]['type'] == 'group') or 'units' in cfg_tmp[k]:
            dic = cfg_groups[k] = cfg_tmp.pop(k)
            dic['type'] = 'group'
        else:
            dic = cfg_repos[k] = cfg_tmp.pop(k)
            dic['type'] = 'repo'
        dic['id'] = k

    # Assign parents property to ids
    for k in list(cfg_groups.keys()):
        for r in cfg_groups[k]["units"]:
            dic = get_by_id_dic(r)
            if not dic:
                dic = cfg_repos[r] = { 'id': r, 'type': 'repo', 'parent': k }
            if "parents" not in dic: dic["parents"] = []
            dic["parents"].append(k)

    id_keys = list(cfg_groups.keys())
    id_keys.extend(list(cfg_repos.keys()))

    # Find parent
    for k in id_keys:
        dic = get_by_id_dic(k)
        if 'parents' not in dic or not dic['parents']:
            dic['parent'] = 'global'
            if dic['type'] == 'repo':
                dic['parents'] = ['orphan']
                cfg_groups['orphan']['units'].append(k)
            else:
                dic['parents'] = ['global']
        else:
            if 'parent' not in dic or not dic['parent']:
                dic['parent'] = dic['parents'][0]

    # setup defaults
    for k in id_keys: cfg_set_default_id(k)

    return 0
def cmd_status(dic):
    if dic['type'] == 'group': return
    # change to repo path and execute '<vcs> status'
    ret = sp.Popen([dic['vcs'],'status'], cwd=dic['path'])
    ret.wait()
    if ret.returncode: return (False, dic['id'])
    return (True, dic['id'])

def cmd_info(dic):
    for k in ['path', 'vcs', 'parent', 'parents', 'desc']:
        print("%s: %s"%(k,dic[k]))
    if 'units' in dic and dic['units']:
        print("units: %s"%pformat(dic['units']))
def cmd_cmds(dic):
    ls_err = []
    if dic['type'] == 'group': return
    if not dic['cmds']: return
    for c in dic['cmds']:
        cli = dic['vcs'] + ' ' + c
        print("-- command: %s"%(cli))
        ret = sp.Popen(cli.split(), cwd=dic['path'])
        ret.wait()
        if ret.returncode: ls_err.append(cli)
    return ls_err
def cmd_sync(dic):
    cmd_fetch(dic)
    cmd_pull(dic)
    cmd_push(dic)

def cmd_fetch(dic):
    pass
def cmd_pull(dic):
    pass
def cmd_push(dic):
    pass
def cmd_on_id(key):
    dic = get_by_id_dic(key)
    if not dic:
        print("Unknown object: %s"%(o))
        return
    print("== %s: %s =="%(dic['type'],get_by_id_ptree(key)))
    if dic['type'] == 'group':
        if g_cmd == 'info': cmd_info(dic)
        elif g_cmd == 'list': return
        else:
            for u in dic['units']: cmd_on_id(u)
    else: eval("cmd_%s(dic)"%(g_cmd))
# Main
def main(argv):
    global g_cmd, g_objs, g_obj_all, cfg_repos, cfg_groups
    if len(argv) < 2 or cli_options(argv[1:]) != 0:
        print(__doc__ % argv[0])
        exit(0)
    n_err = config_reader()
    if n_err != 0:
        print("Error: %s"%msg_ret[n_err])
        return
    # command
    if g_obj_all: g_objs = list(cfg_repos.keys())
    for o in g_objs: cmd_on_id(o)
#-----------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv)

