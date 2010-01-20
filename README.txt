            ``app-envsel'' -- multi-version handler for applications
            ========================================================

Author: Exaos Lee (PGP: 57D75560) <Exaos.Lee@gmail.com>
Date: 2010-01-20 15:33:04 CST


Introduction 
=============

Purpose 
--------
   To organize multi-versions of one application and let user easily select
   their preferred one. It's intended to run on some unix-like systems with many
   applications and users, such as a Linux cluster.

License: GPLv3 
---------------

Links 
------
   1. Git repository: [http://github.com/exaos/app-envsel]
   2. Author's ID: [http://exaos.myopenid.com/]

How to use app-envsel 
======================

Install and setup 
------------------
   + Install
     1. Copy app-envsel.py to the directory in your PATH setting
     2. chmod +x app-envsel.py
     3. ln -s app-envsel.py app-envsel
   + Initialization
     System-wide setup:  app-envsel init -s
     User-wide setup  :  app-envsel init -u
   + Setup application data
     - Add one application version
       * command: app-envsel register/reg <app> <version>
     - Delete one application version
       * command: app-envsel remove/rm <app> <version>
     - Remove all versions of one application
       * command: app-envsel remove/rm <app> -a

User commands 
--------------
   + List application's versions
     - command: app-envsel list/ls [opt] [<app>]
     - options: -s --- short list
   + Set version for <app>
     - command: app-envsel set [opt] <app> <ver>
     - options: -s --- system-wide
   + Unset version for <app>
     - command: app-envsel unset [opt] [<app>]
     - options: -s --- system-wide

----------------------------------------------------------------------

Code information 
=================
  + app-envsel.py
    - check both system- and user-wide data directory
    - check both system- and user-wide setting for one app
    - command processing
    - Structure
      * `app_envdata' --- Class to handle the environment repository
        + `set_datadir'
        + `init_datadir'
        + `check_apprc'
        + `check_datadir'
        + `check_sh_rc'
        + `check_envsel'
        + `remove'
        + `register'
        + `list_all'
      * `app_envsel'  --- Class to handle one application
        + `check_envsel'
        + `remove'
        + `register'
        + `list'
        + `set'
        + `unset'
      * `cmd_process' --- Command parser and processor
  + Data structure
    - Versions startup script is stored in data dir as `<app>_<ver>.sh'
    - System- or user-wide selection is write to file `<env-path>/<app>'
  + app-rc.sh
    - encoded the zipped content in base64, and added to app-envsel.py
    - First check user's setting then system's
    - First check user's versions then system's

Changelog 
==========
  + 2010-01-12: Finish all features planned first, only bash supported.
  + 2010-01-07: Initialized project.

----------------------------------------------------------------------

