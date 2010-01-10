#!/usr/bin/env python
'''
Usage: env-selector <command> [app] [options]

Commands:
  init
  register
  unregister
  remove
  list
  set
  unset
'''

import os, sys
import os.path as path

# Check the data path
app_data_sys = "/var/lib/app-envsel/data"
app_env_sys  = "/var/lib/app-envsel/env"
app_data_user= path.join(os.environ['HOME'],'.config/app-envsel/data')
app_env_user = path.join(os.environ['HOME'],'.config/app-envsel/env')

class app_envdata:
    _start_sh = dict()
    _isChecked = False
    _isSystem  = False

    def __init__(self):
        # Check data dir
        self._data_dir = ""
        if path.isdir(app_data_sys):    self._data_dir = app_data_sys
        elif path.isdir(app_data_user): self._data_dir = app_data_user
        else:
            print "Neither system- nor user-wide data directory exists!"
            return

        self.check_datadir()
        self.check_env_sys()
        self.check_env_user()
        self._app_rc = path.join(self._data_dir,"app-rc")

    def init_datadir(self): pass

    def check_datadir(self):
        '''Check the data directory to collect versions of application'''
        rdata = os.listdir(self._data_dir)
        apps = set([f.split('_') for f in rdata])
        self._apps = dict()
        for a in apps:
            flist = filter(lambda x: x[:len(a)] == a, rdata)
            finfo = a+'_info'
            if finfo not in flist: finfo = ""
            flist.remove(finfo)
            vers = set([ f[:f.rfind('.')] for f in flist ])
            self._apps[a] = [finfo, vers]
        self._isChecked = True

    def check_envsel(self, env_dir):
        '''Check the current environment selections for apps'''
        envsel = dict()
        if not path.isdir(env_dir): return envsel

        rdata = os.listdir(env_dir)
        apps  = set([f.split('_') for f in rdata])
        for a in apps: envsel[a] = filter(lambda x: x[:len(a)]==a, rdata)
        return envsel

    def check_env_user(self):
        if not self._isSystem:
            self._envsel = self.check_envsel(app_env_user)

    def check_env_sys(self):
        self._envsel_sys = self.check_envsel(app_env_sys)

    def check_sh_rc(self, u_shrc='.bashrc', a_shrc='app-rc'):
        f_rc_u = path.join(os.environ['HOME'],u_shrc)
        f_rc_a = self._app_rc + '.sh'
        rc_sappend = '[ -f %s ] && . %s\n'%(f_rc_a, f_rc_a)
        rc_script = open(f_rc_u).readlines()
        if rc_sappend in rc_script:
            print "Env code has already been added to your startup script."
        else:
            print "Writing env code to your startup script ..."
            open(f_rc_u,'a+').write(rc_sappend)

class app_envsel(app_envdata):
    '''
    Class to manage evironments for one certain application.
    Properties:
      _name     --- application's short name
      _lname    --- application's long name
      _desc     --- application's description
      _start_sh --- the startup shells
    '''
    def __init__(self,**kws):
        if not kws.has_key("name"):
            print "** ERROR **: you must provide the application's name"
            return
        self._name = kws['name']
        if kws.has_key('lname'): self._lname = kws['lname']
        if kws.has_key('desc'):  self._desc  = kws['desc']

        # System-wide setting or not?
        if kws.has_key('isSys'): self._isSystem = kws['isSys']
        if self._isSystem:  self._env_dir  = app_env_sys
        else:               self._env_dir  = app_env_user

    def init_data(self,name,prefix="",datadir=""): pass
    def remove_data(self): pass
    def register_env(self,ename,envpath): pass
    def unregister_env(self,ename): pass

    def list_env(self): pass
    def set_env(self,ename):   pass
    def unset_env(self,ename): pass

def my_main(a_env_sel, isSYS = False):
    pass

if __name__=='__main__':
    import sys
    if path.isdir(app_data_sys):
        app_data_dir = app_data_sys
    elif path.isdir(app_data_user):
        app_data_dir = app_data_user
    else:
        print "** ERROR **: Neither system-wide nor user-wide data directory exists!"
        sys.exit(1)
    print "Reading data from %s"%(app_data_dir)

