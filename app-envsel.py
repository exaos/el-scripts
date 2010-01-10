#!/usr/bin/env python
'''
Usage: env-selector <app> <command> [options]

Commands:
  list
  set
  register
  unset
  unregister
  remove
  init
'''

import os, sys
import os.path as path

class app_envsel:
    '''
    Class to manage evironments for one certain application.
    Properties:
      _name     --- application's short name
      _lname    --- application's long name
      _desc     --- application's description
      _start_sh --- the startup shells
      _data_dir --- the data directory contains environments
    '''
    _name = ""
    _data_dir = ""
    _start_sh = dict()
    _isChecked = False

    def __init__(self,**kws):
        if not kws.has_key("name"):
            print "** ERROR **: you must provide the application's name"
            return False
        self._name = kws['name']
        if kws.has_key('lname'): self._lname = kws['lname']
        if kws.has_key('desc'):  self._desc  = kws['desc']
        # Default bash startup script must be add!
        if kws.has_key('shartsh'): self._start_sh = kws['startsh']
        if 'bash' not in self._start_sh.keys():
            self._start_sh['bash']='.sh'
        return True

    def check_datadir(self): pass

    def init_data(self,name,prefix="",datadir=""): pass
    def remove_data(self): pass
    def register_env(self,ename,envpath): pass
    def unregister_env(self,ename): pass

    def list_env(self): pass
    def set_env(self,ename):   pass
    def unset_env(self,ename): pass
