#!/usr/bin/python
# coding:utf-8
import sys
# import time
import socket
import httplib
# import urllib
# from bs4 import BeautifulSoup
# import transmissionrpc

from SearchEngine.SearchEngine import ExtractError
from SearchEngine.HaiDaoWan import HaiDaoWan
from SearchEngine.EZTV import EZTV
from SearchEngine.ZiMuKu import ZiMuKu
from SearchEngine.IMDB import IMDB
# from SearchResult.SearchResult import SearchResult
# from WebPageGrabber import WebPageGrabber
# from data import soup

# set output utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

# avoid chunked
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

# set default time to 30 sec
socket.setdefaulttimeout(30)

RED = '\033[31m'
BLUE = '\033[4;;34m'
RESET = '\033[0m'

DOWNLOAD_PATH = '/home/cytosine/Downloads/AuTomtit/'

if __name__ == '__main__':
    SE = [HaiDaoWan(), EZTV(), ZiMuKu(), IMDB()]
    while True:
        print '# input 1: HaiDaoWan'
        print '# input 2: QingSongTV'
        print '# input 3: ZiMuKu'
        print '# input 4: IMDB'
        print '# input anything else to exit'
        print 'please choose which search engine you want to use:',
        num = raw_input()
        try:
           num = int(num)
        except ValueError:
            break
        except IndexError:
            break
        se = SE[num - 1]
        print 'please input key words:',
        key_word = raw_input()
        if se.search(key_word):
            print '# Showing results 10 at a time'
            print '# press enter to show next 10 results'
            print '# or input \'exit\' to exit'
            print '-' * 70
            try:
                for i, result in enumerate(se.results()):
                    index = i + 1
                    print '# Number:', index
                    print result, '-' * 70
                    result.download(DOWNLOAD_PATH + key_word + ' ' + str(index) + '/')
                    if (index % 10) == 0:
                        if raw_input() == 'exit':
                            break
                else:
                    print 'No more results!'
            except ExtractError:
                print RED + 'Can\'t parse the web page' + RESET
                continue
        else:
            print 'No Results!'
