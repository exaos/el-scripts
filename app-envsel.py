#!/usr/bin/env python
'''
Usage: app-envsel <command> [app] [options]

Commands:
  init         ---  setup the environment for app-envsel
  register/reg ---  register verion to certain application
  remove/rm    ---  remove one or all versions of certain application
  list/ls      ---  list versions of certain application
  set          ---  choose one version for certain application
  unset        ---  unset one version for certain application

Author: Exaos Lee <Exaos.Lee(at)gmail.com>, Jan. 2010
'''
import os, sys
import os.path as path
from base64   import b64decode
from zlib     import decompress

# Check the data path
data_dir_sys  = "/var/lib/app-envsel"
data_dir_user = path.join(os.environ['HOME'],'.config/app-envsel')

# app-rc.sh
app_rc_enc='''
eJyVVGFv2jAQ/Vz/iiOgikhLAvtIx7SoybZKjE6FaZoA0UAMWAp2ZJtojOW/zzYhZJRMa5AS
53j37vnuOc2GtyDUW0Rig5pwz9I9J+uNhPbShredbgfCnxETMMAY3pmlq5btSNrrbUQSd8m2
79/A/TAYoKbK/7rjKRO4B2MGKWcZiTHIDQYhIy53KWCaEc7oFlMJK8YhSlNHxQROEPLDeeCP
/fnox6jvZRH3ErLwzgAvjmSkQaNwHNSC1KMk+jYKn/qtz49fQk/ppCuyrqX7N1STIoHlXC3a
NjogUJf6n/ZbXbMmK5iAs4LWoUqYey0Ngtmd7gFFN+ot67faAsfgTZteXIP/DRrhUOimtqFf
kUqVX2BpWGbBDG5vL+uqvrymbAVeVxUvN0yHrRGWktA1GHgPrJc7L7uuOA8alc/NM8tdsTnr
KRlrk3SOTnFdVebG/Q/2gtWaBI/DcHbUhpOX6o4bfp24v3PqtdVwn6RpZY2TMoFLxR/9h0EY
FJqLpu+ospuxmL5lKEfI7KUBTnxREZzoMmyaVG6pHKL13X8aPgw/9SBQ3oeYcLyUjO+BCKBM
AsdRvDfHcmqd3T+1lGgjWBNNykqlf5QPtRFVhj4fc7EXymyJAMe/ANrXGAqtVYadwPwKhUHa
6HT45gkRst9+Nlsz3S6T88q7kpMrb0sOlv5NqaWdzrgEZwfP9tnErUPzxKp6upbQOZui+FQB
oQWzRk0+zHK4g5hB8WkwJ0MHqBpuOcGrYzUESEXRMVRMDiqDheo0z7BTN6HaFoT+ACSbwKs=
'''

class app_envdata:
    _start_sh  = dict()
    _isOK  = False

    def __init__(self, base_dir="", isSys=False):
        self._isSys = isSys
        if base_dir != "": self.set_datadir(base_dir)

    def set_datadir(self, base_dir):
        self._base_dir = base_dir
        self._data_dir = path.join(base_dir, "data")
        self._env_dir  = path.join(base_dir, "env")
        self._app_rc = path.join(self._base_dir,"app-rc")
        if path.isdir(self._data_dir): self.check_datadir()

    def init_datadir(self):
        print "Initializing app-envsel data directory", self._base_dir, "..."
        if not path.isdir(self._data_dir):
            print "\tCreating", self._data_dir, "..."
            os.makedirs(self._data_dir)
        if not path.isdir(self._env_dir):
            print "\tCreating", self._env_dir, "..."
            os.makedirs(self._env_dir)
        self.check_apprc()
        self.check_sh_rc()

    def check_apprc(self):
        f_apprc = self._app_rc + ".sh"
        if not path.isfile(f_apprc):
            print "\tGenerating %s ..."%(f_apprc)
            app_rc_real=decompress(b64decode(app_rc_enc.replace('\n','')))
            open(f_apprc,'w').write(app_rc_real)

    def check_datadir(self):
        '''Check the data directory to collect versions of application'''
        if not path.isdir(self._data_dir):
            print "ERROR: repository %s is not initialized!"%(self._base_dir)
            return
        rdata = os.listdir(self._data_dir)
        apps = set([f.split('_')[0] for f in rdata])
        self._apps = dict()
        for a in apps:
            flist = filter(lambda x: x[:len(a)] == a, rdata)
            finfo = a+'_info'
            if finfo not in flist: finfo = ""
            else: flist.remove(finfo)
            aa = set([ f[:f.rfind('.')] for f in flist ])
            vers = [ i[i.find('_')+1:] for i in aa ]
            self._apps[a] = [finfo, vers]
        self._isOK = True

    def check_sh_rc(self, u_shrc='.bashrc', a_shrc='app-rc'):
        f_rc_u = path.join(os.environ['HOME'],u_shrc)
        f_rc_a = self._app_rc + '.sh'
        rc_sappend = '[ -f %s ] && . %s'%(f_rc_a, f_rc_a)
        rc_script = [ l.strip() for l in open(f_rc_u).readlines() ]
        if rc_sappend in rc_script:
            print "Env code has already been added to", f_rc_u
        else:
            print "Writing env code to %s ..."%(f_rc_u)
            open(f_rc_u,'a+').write("\n%s\n"%(rc_sappend))

    def check_envsel(self):
        '''Check the current environment selections for apps'''
        self._envsel = dict()
        if not path.isdir(self._env_dir): return None
        apps = os.listdir(self._env_dir)
        for a in apps:
            fn = path.join(self._env_dir, a)
            vv = filter(lambda x: x[0]!='#',
                        [l.strip() for l in open(fn).readlines()])
            if len(vv)>0: self._envsel[a] = vv[0]

    def remove(self,app,ver="",isAll=False):
        self.check_datadir()
        if app == "": return
        if not self._apps.has_key(app):
            print "Repository has no version for",app
            return
        if isAll: # Remove all settings for app
            for v in self._apps[app][1]:
                fn = path.join(self._data_dir, app+"_"+v+".sh")
                print "Removing file",fn
                os.remove(fn)
            fn = path.join(self._env_dir, app)
            if path.isfile(fn): os.remove(fn)
        else:
            if ver == "":
                print "Null version"
                return
            if ver in self._apps[app][1]:
                fn = path.join(self._data_dir, app+"_"+ver+".sh")
                print "Removing file",fn
                os.remove(fn)
            else:
                print "Version %s:%s is not in repository!"%(app,ver)

    def register(self, app, ver, vpath):
        if app == "" or ver == "" or vpath == "": return
        fname = path.join(self._data_dir, app+"_"+ver+".sh")
        status = os.system("cp %s %s"%(vpath, fname))
        if status != 0:
            print "Failed to register %s_%s"%(app,ver)

    def get_list(self, app):
        if app == "": return
        if app not in self._apps:
            print "Warning: %s is not in env-data"%(app)
        else: return self._apps[app]

    def list(self):
        self.check_datadir()
        for app in self._apps.keys():
            print app,":",self._apps[app][1]

    def list_long(self):
        self.check_datadir()
        self.check_envsel()
        if self._isSys: r_mark = "s"
        else: r_mark = "u"
        for app in self._apps.keys():
            vsel = ""
            if self._envsel.has_key(app): vsel = self._envsel[app]
            print "\n-------- Application: %s"%(app)
            print "Info file:",
            if self._apps[app][0] != "":
                print path.join(self._data_dir,self._apps[app][0])
            else: print "Not set"
            vlen = len(self._apps[app][1])
            print "Versions available:",
            if vlen==0: print "None"
            else:
                print vlen
                for v in self._apps[app][1]:
                    if vsel == v: m_sel = "*"
                    else: m_sel = " "
                    print "  %s%s  %s"%(r_mark,m_sel,v)
        print

class app_envsel:
    '''
    Class to manage evironments for one certain application.
    Properties:
      _name     --- application's short name
    '''
    def __init__(self,**kws):
        if not kws.has_key("name"):
            raise Exception("App's name must be provided!")
        self._name = kws['name']
        if kws.has_key('repo'):  self._repo  = kws['repo']
        if not self._repo:
            raise Exception("App's env repository must be given!")
        self._elist = self._repo.get_list(self._name)

        if kws.has_key('edir'): self._dir = kws['edir']
        else: self._dir = path.join(data_dir_user,"env")
        self._fsel = path.join(self._dir, self._name)

        if kws.has_key('finfo'): self._finfo = kws['finfo']
        elif self._elist: self._finfo = self._elist[0]

    def check_envsel(self):
        self._vset = ""
        if path.isfile(self._fsel):
            aa = filter(lambda x: x[0]!='#',
                        [l.strip() for l in open(self._fsel).readlines()])
            if len(aa)>0: self._vset = aa[0]

    def remove(self,aver="",allVer=False):
        if env == "" and allVer:
            self._repo.remove(self._name,ver="",isAll=True)
        elif env != "" and ver in self._elist[1]:
            self._repo.remove(self._name,ver=aver)
        else: return

    def register(self,ver,vpath): self._repo.register(self._name,ver,vpath)
    def list(self):
        if not self._elist or len(self._elist[1]) == 0:
            print "No version found for", self._name
            return
        self.check_envsel()
        self._repo.check_envsel()
        if self._repo._isSys: r_mark = "*"
        else: r_mark = "-"
        for v in self._elist[1]:
            sel_u, sel_s = " ", " "
            if v == self._vset: sel_u = "U"
            if self._repo._envsel.has_key(self._name):
                if self._repo._isSys and v == self._repo._envsel[self._name]:
                    sel_s = "S"
            print "%s%s%s  %s"%(r_mark, sel_s, sel_u, v)

    def set(self,ver):
        if ver in self._elist[1]:
            open(self._fsel,'w').write("%s\n"%(ver))
        else:
            print "Version %s is not in repository"%(ver)
    def unset(self,ver=""):
        self.check_envsel()
        if self._vset == ver or ver == "":
            print "Removing %s ..."%(self._fsel)
            os.remove(self._fsel)

def cmd_process(args):
    arglen = len(args)
    if arglen==0 or args[0]=="":
        print __doc__
        return

    errmsg = ["ERROR: Neither system nor user environemnt repository is found!",
              "ERROR: System repository is not setup properly!",
              "ERROR: User repository is not setup properly!",]
    if path.isdir(path.join(data_dir_sys,'data')):
        repo_sys  = app_envdata(data_dir_sys,isSys=True)
    else: repo_sys = None
    if path.isdir(path.join(data_dir_user,'data')):
        repo_user = app_envdata(data_dir_user)
    else: repo_user = None
    if args[0] != "init" and not repo_sys and not repo_user:
        print errmsg[0]
        return

    # init
    if args[0]=="init":
        if arglen<2:
            print "Usage: app-envsel init <-s/-u>"
            print "  -s   ---  system-wide initial"
            print "  -u   ---  user-wide initial"
        elif args[1]=="-s": # system-wide init
            app_envdata(data_dir_sys).init_datadir()
        else:  # user-wide init
            app_envdata(data_dir_user).init_datadir()

    # register/reg
    elif args[0]=="register" or args[0]=="reg":
        usage = "Usage: app-envsel register <app> <ver> <path-to-ver-sh>"
        if arglen<4:
            print usage
            return
        else: # register <app> <path-to-ver-sh>
            if repo_sys and repo_sys._isOK:
                print "Registering %s:%s to system repository ..."%(args[1], args[2])
                repo_sys.register(args[1], args[2], args[3])
            elif repo_user and repo_user._isOK:
                print "Registering %s:%s to user repository ..."%(args[1], args[2])
                repo_user.register(args[1], args[2], args[3])
            else:
                print errmsg[0]
                return

    # remove/rm
    elif args[0]=="remove" or args[0]=="rm":
        usage = '''Usage: app-envsel remove <app> <-a | ver>'''
        if arglen<3:
            print usage
        else:
            ver, isAll = "", False
            if args[2] == "-a": isAll = True
            else: ver = args[2]
            if repo_sys and repo_sys._isOK:
                repo_sys.remove(args[1],ver=ver,isAll=isAll)
            if repo_user and repo_user._isOK:
                repo_user.remove(args[1],ver=ver,isAll=isAll)

    # list/ls
    elif args[0]=="list" or args[0]=="ls":
        if arglen<2: # List all apps
            if repo_sys  and repo_sys._isOK:  repo_sys.list_long()
            if repo_user and repo_user._isOK: repo_user.list_long()
        elif args[1]=='-s':
            if repo_sys  and repo_sys._isOK:  repo_sys.list()
            if repo_user and repo_user._isOK: repo_user.list()
        else: # List <app>
            if repo_sys and repo_sys._isOK:
                app_envsel(name=args[1],repo=repo_sys).list()
            if repo_user and repo_user._isOK:
                app_envsel(name=args[1],repo=repo_user).list()

    # set
    elif args[0]=="set":
        if arglen<3:
            print "Usage: app-envsel set <app> [-s] <ver>"
            print "Option: -s  --- set the system-wide version"
        else:
            isSys = False
            if arglen>3 and args[2]=="-s": # system-wide
                isSys = True
                ver = args[3]
                env_dir = path.join(data_dir_sys,"env")
            else: # User-wide
                env_dir = path.join(data_dir_user,"env")
                ver = args[2]
            if isSys:
                if not repo_sys or repo_sys._isOK:
                    print errmsg[1]
                    return
                repo = repo_sys
            else:
                if repo_sys and repo_sys._isOK: repo=repo_sys
                elif repo_user and repo_user._isOK: repo=repo_user
            asel = app_envsel(name=args[1],repo=repo,edir=env_dir)
            asel.set(ver)

    # unset
    elif args[0]=="unset":
        if arglen<2:
            print "Usage: app-envsel unset <app> [-s]"
            print "Option: -s  --- unset the system-wide version"
        else:
            isSys = False
            if arglen>2 and args[2]=="-s": # system-wide
                if not repo_sys or repo_sys._isOK:
                    print errmsg[1]
                    return
                isSys = True
                repo = repo_sys
                env_dir = path.join(data_dir_sys,"env")
            else: # User-wide
                if repo_sys and repo_sys._isOK: repo = repo_sys
                elif repo_user and repo_user._isOK: repo = repo_user
                env_dir = path.join(data_dir_user,"env")
            asel = app_envsel(name=args[1],repo=repo,edir=env_dir)
            asel.unset()

    # Display help
    else: print __doc__

if __name__=='__main__':
    import sys
    cmd_process(sys.argv[1:])
