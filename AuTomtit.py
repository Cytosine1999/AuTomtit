#!/usr/bin/python
import os
import json


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
    f = file(DIR, 'w')
    json.dump(profile, f, sort_keys=True, indent=4, separators=(',', ':'))
    f.close()
    PROFILE = profile


if __name__ == '__main__':
    from WebCrawler import WebCrawler
    WebCrawler.search()
