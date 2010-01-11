#!/usr/bin/env python
'''
Usage: app-envsel <command> [app] [options]

Commands:
  init       ---  setup the environment for app-envsel
  register   ---  register verion to certain application
  remove     ---  remove one or all versions of certain application
  list       ---  list versions of certain application
  set        ---  choose one version for certain application
  unset      ---  unset one version for certain application

Author: Exaos Lee <Exaos.Lee(at)gmail.com>, Jan. 2010
'''
import os, sys
import os.path as path
from base64   import b64decode
from zlib     import decompress

# Check the data path
app_data_sys = "/var/lib/app-envsel/data"
app_env_sys  = "/var/lib/app-envsel/env"
app_data_user= path.join(os.environ['HOME'],'.config/app-envsel/data')
app_env_user = path.join(os.environ['HOME'],'.config/app-envsel/env')
# app-rc.sh
app_rc_enc='''
eJyVVGFv2jAQ/Vz/isOgikgLKfvYLpNQybRJrJ0W9mEaVRqIAUtgR7ahYyz/fT4HkpTBpAkp
2Jd3757vndNuBVMugmmql6QN9zLfKb5YGujOPHh707+B6GcqNYwYg3du2bPLbmq8xTrlq95M
rt+/gfuH4Yi0bX6804at/ReeMUjzPFGznl7CXCrc+UxsNVtZ2JeNyqVmtzCWkCu5RbhZMtAm
VWaTgwVyJcWaCXOaTAZRMhyMB0n8PQ6DbaqCFZ8GNSDIUpMiKI7Gw4sg+1cRfYujr2Hn4+Pn
KLDHEXO+uEj3byiSkh/gZ9DZN1QW8ATX13CIhK/fIf4X0CpYUIBLeKxeEKKZSWyprkf2xIKx
OSLs9N2az8ESzksBleQi6CAInu6wy4Jc2d027HQ1yyCYtIPsAv43IMIX0M89Rz/njSooG4lo
qfekLh7uP8o24JeqstlSYpjGzBguFuDgt3WzLcEeQ0XidOHk9XpA/25MA7wtEFYp7J1lq4Dk
yomgw8eHqFUSs5Vmx/CHwadRNKRN0Rth7XIW4WNLrH9OSuvVmBSVguqgdGgHDzKu2MxItQOu
QUgDyIY3YkLrwZtQSpwMTK7nr+qr9QcNwvtoExK909aElQZ/cAL0zjG4gSgtPjJsNFNnKBzS
I8ehTFZcm7D77I7jelglF429lVNYz40Cir+JoDgBUhnwN/Ds1e519u0jawH+wsBN7dvhIwFc
HJhL1B1kEg73xY0LBoT1q7LlrFcum9goKUMHl6BxcaF5KWvYsZXQ7AkhfwDvIqFK
'''
app_rc_real=decompress(b64decode(app_rc_enc.replace('\n','')))

class app_envdata:
    _start_sh  = dict()
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

        apps = os.listdir(env_dir)
        for a in apps: envsel[a] = "".join(open(a).readlines()[0]).strip()
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


def cmd_process(args):
    arglen = len(args)
    if arglen==0 or args[0]=="":
        print __doc__
        return

    # init
    if args[0]=="init":
        if arglen<2:
            print "Usage: app-envsel init <-s/-u>"
            print "  -s   ---  system-wide initial"
            print "  -u   ---  user-wide initial"
        elif args[1]=="-s": # system-wide init
            pass
        else:  # user-wide init
            pass
    # register/reg
    elif args[0]=="register" or args[0]=="reg":
        if arglen<3:
            print "Usage: app-envsel register <app> <path-to-ver-sh>"
            return
        else: # register <app> <path-to-ver-sh>
            pass
    # remove/rm
    elif args[0]=="remove" or args[0]=="rm":
        if arglen<2:
            print "Usage: app-envsel remove <app> <option>"
            print "Option:"
            print "   <ver>   --- remove specfic version"
            print "   -a      --- remove all versions"
        else:
            pass
    # list/ls
    elif args[0]=="list" or args[0]=="ls":
        if arglen<2 or args[1]=="-a": # List all apps
            pass
        else: # List <app>
            pass
    # set
    elif args[0]=="set":
        if arglen<3:
            print "Usage: app-envsel set <app> [-s] <ver>"
            print "Option: -s  --- set the system-wide version"
        else:
            if arglen>3 and args[2]=="-s": # system-wide
                pass
            else: # User-wide
                pass
    # unset
    elif args[0]=="unset":
        if arglen<3:
            print "Usage: app-envsel unset <app> [-s] <ver>"
            print "Option: -s  --- unset the system-wide version"
        else:
            if arglen>3 and args[2]=="-s": # system-wide
                pass
            else: # User-wide
                pass
    else:
        print __doc__

if __name__=='__main__':
    import sys
    if path.isdir(app_data_sys):
        app_data_dir = app_data_sys
    elif path.isdir(app_data_user):
        app_data_dir = app_data_user
    else:
        print "** ERROR **: Neither system-wide nor user-wide data directory exists!"
        print "You need to run: app-envsel init [-s|-u]"
        sys.exit(1)
    cmd_process(sys.argv[1:])
