#!/usr/bin/env python

import json
import os
import os.path as path

d_tree = json.load(open("base_tree.json"))

def gen_tree_list(dtree,parent=''):
    t_list = []
    if type(dtree)==unicode:
        return [path.join(parent,dtree),]
    elif type(dtree)==list:
        for d in dtree: t_list.extend(gen_tree_list(d,parent))
    elif type(dtree)==dict:
        for d in dtree.keys():
            t_list.extend(gen_tree_list(dtree[d],path.join(parent,d)))
    else: pass
    return t_list

def mk_base_tree(base='',mode=0755):
    for d in gen_tree_list(d_tree):
        dname = path.join(base,d)
        print("Creating %s ..."%dname)
        os.makedirs(dname,mode)

