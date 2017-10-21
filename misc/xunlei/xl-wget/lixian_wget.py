#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Time-stamp: <2011-11-25 18:54:25 Friday by roowe>
#File Name: thuner_xl_with_wget.py
#Author: bestluoliwe@gmail.com
#My Blog: www.iroowe.com

import re
import time
import os
import logging
import sys
from htmlentitydefs import entitydefs
import subprocess
LOG_FILE = os.path.expanduser("~/thuner_with_wget.log")
log = None


def log_init(log_file, quiet=False):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    hdlr = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    if not quiet:
        hdlr = logging.StreamHandler()
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
    return logger


def handle_entitydef(matchobj):
    key = matchobj.group(1)
    if entitydefs.has_key(key):
        return entitydefs[key]
    else:
        return matchobj.group(0)


def collect_urls(html, only_bturls=False):
    """
    collect urls
    """
    urls = []
    for name, url in re.findall(
            r"<a.+?name=['\"]bturls['\"] title=['\"](.+?)['\"].+?href=['\"](http.+?)['\"]>",
            html):
        name = re.sub("&(.*?);", handle_entitydef, name)
        url = re.sub("&(.*?);", handle_entitydef, url)
        urls.append((name, url))
    if not only_bturls:
        for id, name in re.findall(
                r'<input id=[\'"]durl(\w+?)[\'"].+title=[\'"](.+?)[\'"].+',
                html):
            result = re.search(
                r'<input id=[\'"]dl_url%s[\'"].+value=[\'"](http.*?)[\'"]' %
                id, html)
            if result:
                name = re.sub("&(.*?);", handle_entitydef, name)
                url = result.group(1)
                url = re.sub("&(.*?);", handle_entitydef, url)
                urls.append((name, url))
    log.info("Filter get %d links" % len(urls))
    return urls


def collect_urls_with_cloud(html):
    urls = []
    for id, name in re.findall(
            r'<input id=[\'"]durl(\w+?)[\'"].+title=[\'"](.+?)[\'"].+', html):
        result = re.search(
            r'<input id=[\'"]cloud_dl_url%s[\'"].+value=[\'"](http.*?)[\'"]' %
            id, html)
        if result:
            name = re.sub("&(.*?);", handle_entitydef, name)
            url = result.group(1)
            url = re.sub("&(.*?);", handle_entitydef, url)
            urls.append((name, url))
    log.info("Filter get %d cloud links" % len(urls))
    return urls


def choose_download(urls):
    download_list = {}
    for name, url in urls:
        while True:
            ans = raw_input("Download %s?[Y/n](default: Y) " % name)
            if len(ans) == 0:
                ans = True
                break
            elif ans.lower() == 'y':
                ans = True
                break
            elif ans.lower() == 'n':
                ans = False
                break
            else:
                sys.stdout.write("please enter y or n!\n")
                continue
        download_list[name] = ans
    return download_list


def thuner_xl_with_wget(urls,
                        output_dir,
                        cookies_file,
                        limit_rate=None,
                        quiet=False):
    download_list = choose_download(urls)
    for name, url in urls:
        if len(url) == 0:
            log.debug("Empty Link, Name: " + name)
            continue
        if not download_list[name]:
            continue
        cmd = [
            "wget", "--load-cookies", cookies_file, "-c", "-t", "5", "-U",
            "Mozilla", "-O",
            os.path.join(output_dir, name), url
        ]
        if quiet:
            cmd.insert(1, "-q")
        if limit_rate:
            cmd.insert(1, "--limit-rate=" + limit_rate)
        log.info("wget cmd: '%s'" % ' '.join(cmd))
        ret = subprocess.call(cmd)
        if ret != 0:
            log.debug("wget returned %d." % ret)
            if ret in (3, 8):
                log.error(
                    "Give up '%s', may be already finished download, or something wrong with disk."
                    % name)
            else:
                urls.append((name, url))
                log.error("will retry for %s later." % name)
            continue
        else:
            log.info("Finished %s" % name)
        time.sleep(2)


def thuner_xl_with_aria2c(urls, output_dir, cookies_file, quiet=False):
    """
    download with aria2c
    """
    download_list = choose_download(urls)
    for name, url in urls:
        if len(url) == 0:
            log.debug("Empty Link, Name: " + name)
            continue
        if not download_list[name]:
            continue
        cmd = [
            "aria2c", "--load-cookies", cookies_file, "-d", output_dir, "-c",
            "-m", "5", "-s", "5", "-o", name, url
        ]
        if quiet:
            cmd.insert(1, "-q")
        log.info("wget cmd: '%s'" % ' '.join(cmd))
        ret = subprocess.call(cmd)
        if ret != 0:
            log.debug("wget returned %d." % ret)
            if ret in (13):
                log.error("Give up '%s', file already existed." % name)
            else:
                urls.append((name, url))
                log.error(
                    "the exit status number is %d, and then will retry for %s later."
                    % (ret, name))
            continue
        else:
            log.info("Finished %s" % name)
        time.sleep(2)


def user_task_page(cookies_file, page_file):
    """
    尝试自动下载我的下载任务表
    """
    #http://dynamic.cloud.vip.xunlei.com/user_task?userid=127997030&st=0
    page_url = "http://dynamic.cloud.vip.xunlei.com/user_task?userid=127997030&st=0"
    cmd = [
        "wget", "--load-cookies", cookies_file, "-t", "5", "-U", "Mozilla",
        "-O", page_file, page_url
    ]
    ret = subprocess.call(cmd)
    if ret != 0:
        log.info("Can't get user task page")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Thuner li xian with wget',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-p', nargs='?', default="/tmp/user_task.html", help="load page file")
    parser.add_argument(
        '-c', nargs='?', default="/tmp/cookies.txt", help="load cookie file")
    parser.add_argument('-o', nargs='?', default="/tmp/", help="output dir")
    parser.add_argument('-r', nargs='?', default=None, help="limit rate")
    parser.add_argument(
        '-b', action='store_true', default=False, help="bt files only")
    parser.add_argument(
        '-q',
        action="store_true",
        default=False,
        help="quiet, only log to file.")
    parser.add_argument(
        '-a', action="store_true", default=False, help="download with aria2c")
    parser.add_argument(
        '-u', action="store_true", default=False, help="get user task page")
    parser.add_argument(
        '-y', action="store_true", default=False, help="cloud trans")
    args = parser.parse_args()

    only_bturls, cookies_file, output_dir, page_file, quiet, limit_rate = args.b, args.c, args.o, args.p, args.q, args.r
    if args.y:
        page_file = "/tmp/cloud.html"
    page_file = os.path.expanduser(page_file)
    cookies_file = os.path.realpath(os.path.expanduser(cookies_file))
    output_dir = os.path.expanduser(output_dir)

    log = log_init(LOG_FILE, quiet=quiet)
    if not os.path.exists(cookies_file):
        log.info("please export cookies file")
        sys.exit(0)
    if not os.path.isdir(output_dir):
        log.info("No such %s", output_dir)
        sys.exit(0)
    if args.u:
        user_task_page(cookies_file, page_file)
    with open(page_file) as f:
        page_html = f.read()
    if args.y:
        urls = collect_urls_with_cloud(page_html)
    else:
        urls = collect_urls(page_html, only_bturls)
    if not args.a:
        thuner_xl_with_wget(urls, output_dir, cookies_file, limit_rate, quiet)
    else:
        thuner_xl_with_aria2c(urls, output_dir, cookies_file, quiet)
