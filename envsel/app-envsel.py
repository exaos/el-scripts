#!/usr/bin/env python
'''app-envsel: version manager for applications (Version: 0.1-20100112)

Usage: app-envsel [--sys <path>] <command> [app] [options]

Commands:
  init         ---  setup the environment for app-envsel
  register/reg ---  register verion to certain application
  remove/rm    ---  remove one or all versions of certain application
  list/ls      ---  list versions of certain application
  set          ---  choose one version for certain application
  unset        ---  unset one version for certain application

Options:
  Default system repository is set to /var/lib/app-envsel. If you want an
  alternative path, please use option "--sys <path>" before other commands.

  NOTE: If system repository is other than the default setting, the option
     "--sys <path>" should be added each time you execute this command.

Author: Exaos Lee <Exaos.Lee(at)gmail.com>;  Copyright: GPLv3'''

from __future__ import print_function

import os, sys
import os.path as path

from base64 import b64decode
from zlib import decompress

# Check the data path
data_dir_sysd = "/var/lib/app-envsel"
data_dir_user = path.join(os.environ['HOME'], '.config/app-envsel')

# app-rc.sh
app_rc_enc = '''
eJytVF1v2jAUfa5/xSVEFZGWBPZIxzRUsq0SpRMwTRMgGogBS8GObBONsfz32SZARknZpIF
EnMvxOT73w9WKPyPUn4Vihapwz5ItJ8uVhNrcgbf1Rh2CHyET0MUY3pmlp5a1UDrLdUhib8
7W79/Afa/TRVW1/8uGJ0zgJgwZJJylJMIgVxiEDLncJIBpSjija0wlLBiHMElcFRM4RqgdT
DvtYXs6+D5o+WnI/ZjM/BPAj0IZatAgGHZKQepxJPo6CPot+/PTY+Crc9IFWZbSvQ7VpEhg
OVWLmoN2CNRH/U9bdsOsyQJG4C7A3hUJM9/WIJjc6RxQdKPe0pZdEzgCf1z1oxL8L9AIl0I
jcQz9ghRUfoKlYakFE7i9PddVefkX2QK8THUE9jDoP0KlBVa0Wc9yXTxfMY22BlhKQpdgWJ
pgvUzIsRhKaqdR2dQ808wTq9MxrwmVcmkqzeR5Sv3G+wvR18WsUeepF0z2TnD80ss+a//Fy
p9U5U5KJK8Y0T4qBx8CX7P9sf3QDTq58bz8G6oa3zS7/klRhpBJSAXc6Ox84IbnYVOAY16u
tZP1rd3vPfQ+NaGjhhMiwvFcMr4FIoAyCRyH0dbcG2PrNJ5jS1k09vb87nmDKwUtoXboAZ6
KrVDTEAtw22dA5xJDbqHIsBGYX6AwSAcdbodpTIRs1Z6NNVOy4+as8K6Ok6nhkxws/R1TS4
8i4xLcDTw7p3Gyd9UDq0r1UkL91HD5XQqE5swaNfowyeAOIgb53WVmVAeoaoVjYS9W2xAgF
UX7UF5QKNQbikU+wQ7ZhGJaEPoN89bmkQ==
'''


class app_envdata:
    _start_sh = dict()
    _isOK = False

    def __init__(self, base_dir="", isSys=False):
        self._isSys = isSys
        if base_dir != "": self.set_datadir(base_dir)

    def set_datadir(self, base_dir):
        self._base_dir = base_dir
        self._data_dir = path.join(base_dir, "data")
        self._env_dir = path.join(base_dir, "env")
        self._app_rc = path.join(self._base_dir, "app-rc")
        if path.isdir(self._data_dir): self.check_datadir()

    def init_datadir(self):
        print("Initializing app-envsel data directory", self._base_dir, "...")
        if not path.isdir(self._data_dir):
            print("\tCreating", self._data_dir, "...")
            os.makedirs(self._data_dir)
        if not path.isdir(self._env_dir):
            print("\tCreating", self._env_dir, "...")
            os.makedirs(self._env_dir)
        self.check_apprc()
        self.check_sh_rc()

    def check_apprc(self):
        f_apprc = self._app_rc + ".sh"
        if not path.isfile(f_apprc):
            print("\tGenerating %s ..." % (f_apprc))
            app_rc_real = decompress(b64decode(app_rc_enc.replace('\n', '')))
            if self._isSys and self._base_dir != data_dir_sysd:
                txt = app_rc_real.replace(data_dir_sysd, self._base_dir)
                open(f_apprc, 'w').write(txt)
            else:
                open(f_apprc, 'w').write(app_rc_real)

    def check_datadir(self):
        '''Check the data directory to collect versions of application'''
        if not path.isdir(self._data_dir):
            print("ERROR: repository %s is not initialized!" %
                  (self._base_dir))
            return
        rdata = os.listdir(self._data_dir)
        apps = set([f.split('_')[0] for f in rdata])
        self._apps = dict()
        for a in apps:
            flist = [x for x in rdata if x[:len(a)] == a]
            finfo = a + '_info'
            if finfo not in flist: finfo = ""
            else: flist.remove(finfo)
            aa = set([f[:f.rfind('.')] for f in flist])
            vers = [i[i.find('_') + 1:] for i in aa]
            self._apps[a] = [finfo, vers]
        self._isOK = True

    def check_sh_rc(self, u_shrc='.bashrc', a_shrc='app-rc'):
        f_rc_u = path.join(os.environ['HOME'], u_shrc)
        f_rc_a = self._app_rc + '.sh'
        rc_sappend = '[ -f %s ] && . %s' % (f_rc_a, f_rc_a)
        rc_script = [l.strip() for l in open(f_rc_u).readlines()]
        if rc_sappend not in rc_script:
            print("Writing env code to %s ..." % (f_rc_u))
            open(f_rc_u, 'a+').write("\n%s\n" % (rc_sappend))

    def check_envsel(self):
        '''Check the current environment selections for apps'''
        self._envsel = dict()
        if not path.isdir(self._env_dir): return None
        apps = os.listdir(self._env_dir)
        for a in apps:
            fn = path.join(self._env_dir, a)
            vv = [
                x for x in [l.strip() for l in open(fn).readlines()]
                if x[0] != '#'
            ]
            if len(vv) > 0: self._envsel[a] = vv[0]

    def remove(self, app, ver="", isAll=False):
        self.check_datadir()
        if app == "": return
        if app not in self._apps:
            print("Repository has no version for", app)
            return
        if isAll:  # Remove all settings for app
            for v in self._apps[app][1]:
                fn = path.join(self._data_dir, app + "_" + v + ".sh")
                print("Removing file", fn)
                os.remove(fn)
            fn = path.join(self._env_dir, app)
            if path.isfile(fn): os.remove(fn)
        else:
            if ver == "":
                print("Null version")
                return
            if ver in self._apps[app][1]:
                fn = path.join(self._data_dir, app + "_" + ver + ".sh")
                print("Removing file", fn)
                os.remove(fn)
            else:
                print("Version %s:%s is not in repository!" % (app, ver))

    def register(self, app, ver, vpath):
        if app == "" or ver == "" or vpath == "": return
        fname = path.join(self._data_dir, app + "_" + ver + ".sh")
        status = os.system("cp %s %s" % (vpath, fname))
        if status != 0:
            print("Failed to register %s_%s" % (app, ver))

    def get_list(self, app):
        if app == "": return
        if app not in self._apps:
            print("Warning: %s is not in env-data" % (app))
        else:
            return self._apps[app]

    def list(self):
        self.check_datadir()
        for app in list(self._apps.keys()):
            print(app, ":", self._apps[app][1])

    def list_long(self):
        self.check_datadir()
        self.check_envsel()
        if self._isSys: r_mark = "s"
        else: r_mark = "u"
        for app in list(self._apps.keys()):
            vsel = ""
            if app in self._envsel: vsel = self._envsel[app]
            print("\n-------- Application: %s" % (app))
            print("Info file:", sep=' ')
            if self._apps[app][0] != "":
                print(path.join(self._data_dir, self._apps[app][0]))
            else:
                print("Not set")
            vlen = len(self._apps[app][1])
            print("Versions available:", end=' ')
            if vlen == 0: print("None")
            else:
                print(vlen)
                for v in self._apps[app][1]:
                    if vsel == v: m_sel = "*"
                    else: m_sel = " "
                    print("  %s%s  %s" % (r_mark, m_sel, v))
        print()


class app_envsel:
    '''
    Class to manage evironments for one certain application.
    Properties:
      _name     --- application's short name
    '''

    def __init__(self, **kws):
        if "name" not in kws:
            raise Exception("App's name must be provided!")
        self._name = kws['name']
        if 'repo' in kws: self._repo = kws['repo']
        if not self._repo:
            raise Exception("App's env repository must be given!")
        self._elist = self._repo.get_list(self._name)

        if 'edir' in kws: self._dir = kws['edir']
        else: self._dir = path.join(data_dir_user, "env")
        self._fsel = path.join(self._dir, self._name)

        if 'finfo' in kws: self._finfo = kws['finfo']
        elif self._elist: self._finfo = self._elist[0]

    def check_envsel(self):
        self._vset = ""
        if path.isfile(self._fsel):
            aa = [
                x for x in [l.strip() for l in open(self._fsel).readlines()]
                if x[0] != '#'
            ]
            if len(aa) > 0: self._vset = aa[0]

    def remove(self, aver="", allVer=False):
        if env == "" and allVer:
            self._repo.remove(self._name, ver="", isAll=True)
        elif env != "" and ver in self._elist[1]:
            self._repo.remove(self._name, ver=aver)
        else:
            return

    def register(self, ver, vpath):
        self._repo.register(self._name, ver, vpath)

    def list(self):
        if not self._elist or len(self._elist[1]) == 0:
            print("No version found for", self._name)
            return
        self.check_envsel()
        self._repo.check_envsel()
        if self._repo._isSys: r_mark = "*"
        else: r_mark = "-"
        for v in self._elist[1]:
            sel_u, sel_s = " ", " "
            if v == self._vset: sel_u = "U"
            if self._name in self._repo._envsel:
                if self._repo._isSys and v == self._repo._envsel[self._name]:
                    sel_s = "S"
            print("%s%s%s  %s" % (r_mark, sel_s, sel_u, v))

    def set(self, ver):
        if ver in self._elist[1]:
            if not path.isdir(self._dir):
                print("Creating user selection directory", self._dir)
                os.makedirs(self._dir)
            open(self._fsel, 'w').write("%s\n" % (ver))
            self._repo.check_sh_rc()
        else:
            print("Version %s is not in repository" % (ver))

    def unset(self, ver=""):
        self.check_envsel()
        if self._vset == ver or ver == "" and path.isfile(self._fsel):
            print("Removing %s ..." % (self._fsel))
            os.remove(self._fsel)


def cmd_process(args):
    errmsg = [
        "ERROR: Neither system nor user environemnt repository is found!",
        "ERROR: System repository is not setup properly!",
        "ERROR: User repository is not setup properly!",
    ]
    repo_dir_user = data_dir_user
    if "--sys" in args:
        idx = args.index('--sys')
        if idx < len(args):
            repo_dir_sys = args[idx + 1]
            args.remove("--sys")
            args.remove(repo_dir_sys)
        else:
            print(__doc__)
            return
    else:
        repo_dir_sys = data_dir_sysd

    arglen = len(args)
    if arglen == 0 or args[0] == "":
        print(__doc__)
        return

    if path.isdir(path.join(repo_dir_sys, 'data')):
        repo_sys = app_envdata(repo_dir_sys, isSys=True)
    else:
        repo_sys = None
    if path.isdir(path.join(repo_dir_user, 'data')):
        repo_user = app_envdata(repo_dir_user)
    else:
        repo_user = None
    if args[0] != "init" and not repo_sys and not repo_user:
        print(errmsg[0])
        return

    # init
    if args[0] == "init":
        if arglen < 2:
            print("Usage: app-envsel init <-s/-u>")
            print("  -s   ---  system-wide initial")
            print("  -u   ---  user-wide initial")
        elif args[1] == "-s":  # system-wide init
            app_envdata(repo_dir_sys, isSys=True).init_datadir()
        else:  # user-wide init
            app_envdata(repo_dir_user).init_datadir()

    # register/reg
    elif args[0] == "register" or args[0] == "reg":
        usage = "Usage: app-envsel register <app> <ver> <path-to-ver-sh>"
        if arglen < 4:
            print(usage)
            return
        else:  # register <app> <path-to-ver-sh>
            if repo_sys and repo_sys._isOK:
                print("Registering %s:%s to system repository ..." % (args[1],
                                                                      args[2]))
                repo_sys.register(args[1], args[2], args[3])
            elif repo_user and repo_user._isOK:
                print("Registering %s:%s to user repository ..." % (args[1],
                                                                    args[2]))
                repo_user.register(args[1], args[2], args[3])
            else:
                print(errmsg[0])
                return

    # remove/rm
    elif args[0] == "remove" or args[0] == "rm":
        usage = '''Usage: app-envsel remove <app> <-a | ver>'''
        if arglen < 3:
            print(usage)
        else:
            ver, isAll = "", False
            if args[2] == "-a": isAll = True
            else: ver = args[2]
            if repo_sys and repo_sys._isOK:
                repo_sys.remove(args[1], ver=ver, isAll=isAll)
            if repo_user and repo_user._isOK:
                repo_user.remove(args[1], ver=ver, isAll=isAll)

    # list/ls
    elif args[0] == "list" or args[0] == "ls":
        if arglen < 2:  # List all apps
            if repo_sys and repo_sys._isOK: repo_sys.list_long()
            if repo_user and repo_user._isOK: repo_user.list_long()
        elif args[1] == '-s':
            if repo_sys and repo_sys._isOK: repo_sys.list()
            if repo_user and repo_user._isOK: repo_user.list()
        else:  # List <app>
            if repo_sys and repo_sys._isOK:
                app_envsel(name=args[1], repo=repo_sys).list()
            if repo_user and repo_user._isOK:
                app_envsel(name=args[1], repo=repo_user).list()

    # set
    elif args[0] == "set":
        if arglen < 3:
            print("Usage: app-envsel set <app> [-s] <ver>")
            print("Option: -s  --- set the system-wide version")
        else:
            isSys = False
            if arglen > 3 and args[2] == "-s":  # system-wide
                isSys = True
                ver = args[3]
                env_dir = path.join(repo_dir_sys, "env")
            else:  # User-wide
                env_dir = path.join(repo_dir_user, "env")
                ver = args[2]
            if isSys:
                if not repo_sys or repo_sys._isOK:
                    print(errmsg[1])
                    return
                repo = repo_sys
            else:
                if repo_sys and repo_sys._isOK: repo = repo_sys
                elif repo_user and repo_user._isOK: repo = repo_user
            try:
                asel = app_envsel(name=args[1], repo=repo, edir=env_dir)
                asel.set(ver)
            except:
                print("Failed to set %s:%s!" % (args[1], ver))

    # unset
    elif args[0] == "unset":
        if arglen < 2:
            print("Usage: app-envsel unset <app> [-s]")
            print("Option: -s  --- unset the system-wide version")
        else:
            isSys = False
            if arglen > 2 and args[2] == "-s":  # system-wide
                if not repo_sys or repo_sys._isOK:
                    print(errmsg[1])
                    return
                isSys = True
                repo = repo_sys
                env_dir = path.join(repo_dir_sys, "env")
            else:  # User-wide
                if repo_sys and repo_sys._isOK: repo = repo_sys
                elif repo_user and repo_user._isOK: repo = repo_user
                env_dir = path.join(repo_dir_user, "env")
            try:
                asel = app_envsel(name=args[1], repo=repo, edir=env_dir)
                asel.unset()
            except:
                print("Failed to unset %s current version!" % (args[1]))

    # Display help
    else:
        print("Unknown command:", args[0])
        print(__doc__)


if __name__ == '__main__':
    import sys
    cmd_process(sys.argv[1:])
