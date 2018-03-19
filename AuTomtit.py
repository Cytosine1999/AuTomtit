#!/usr/bin/python
import os
import sys
import json

# set output utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

DIR, _ = os.path.split(os.path.realpath(__file__))
DIR += '/profile.json'

PROFILE = None


def load():
    global PROFILE
    f = file(DIR, 'r')
    if PROFILE is None:
        PROFILE = json.load(f)
    f.close()
    return PROFILE


def dump(profile):
    global PROFILE
    PROFILE = profile


def save():
    global PROFILE
    f = file(DIR, 'w')
    json.dump(PROFILE, f, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
    f.close()


if __name__ == '__main__':
    from WebCrawler import WebCrawler
    WebCrawler.search()
    save()
