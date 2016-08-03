#!/usr/bin/env python2
# -*- coding: utf-8 -*- 
'''
@Exaos
'''

from PIL import Image
from PIL.ExifTags import TAGS
import shutil,os,os.path

def get_exif(fn):
    ret = {}
    img = Image.open(fn)
    info = img._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

def get_isodate(fn):
    exif = get_exif(fn)
    yy = exif['DateTimeOriginal'][:4]
    mm = exif['DateTimeOriginal'][5:7]
    dd = exif['DateTimeOriginal'][8:10]
    return yy,mm,dd

def copy_image_to_isodate_dir(fn):
    destdir = os.path.sep.join(get_isodate(fn))
    try:
        os.makedirs(destdir)
    except OSError:
        pass
    shutil.copy2(fn,destdir)

if __name__ == '__main__':
    import sys
    for fn in sys.argv[1:]:
        print "Copy",fn,"to", os.path.sep.join(get_isodate(fn))
        copy_image_to_isodate_dir(fn)

