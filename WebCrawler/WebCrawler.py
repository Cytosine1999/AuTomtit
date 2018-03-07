#!/usr/bin/python
# coding:utf-8
import sys
# import time
import httplib
# import urllib
# from bs4 import BeautifulSoup
# import transmissionrpc

from SearchEngine.SearchEngine import ExtractError
from SearchEngine.HaiDaoWan import HaiDaoWan
from SearchEngine.EZTV import EZTV
from SearchEngine.ZiMuKu import ZiMuKu
# from SearchResult.SearchResult import SearchResult
# from WebPageGrabber import WebPageGrabber
# from data import soup

# set output utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

# avoid chunked
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

RED = '\033[31m'
BLUE = '\033[4;;34m'
RESET = '\033[0m'

if __name__ == '__main__':
    """
    page_num = int(soup.find(id='page').select('span.pc')[0].string)
    soup.find(id='content_left').select('div')
    """
    """
    wpg = WebPageGrabber()
    respond = wpg.grab_page('http://www.baidu.com/link?url=rVT0BdQQb3IESSyRC2-0hQ6XGM39qEwAwvog7TcojakqgGIS_KApiIxHc-id2Wmf')
    print respond.read()
    # soup = BeautifulSoup(respond.read(), 'html5lib')
    """
    """
    urllib.urlretrieve('http://www.subku.net/download', "demo.zip") 
    """

    while True:
        print '# input 1: HaiDaoWan'
        print '# input 2: QingSongTV'
        print '# input 3: ZiMuKu'
        print '# input anything else to exit'
        print 'please choose which search engine you want to use:',
        SE = [HaiDaoWan(), EZTV(), ZiMuKu()]
        num = raw_input()
        try:
            se = SE[int(num) - 1]
        except ValueError:
            break
        except IndexError:
            break
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
                    # result.download('/home/cytosine/Downloads/AuTomtit/' + key_word + ' ' + str(index) + '/')
                    if (index % 10) == 0:
                        if raw_input() == 'exit':
                            break
                else:
                    print 'No more results!'
            except ExtractError:
                print RED + 'Can\'t parse the web page' + RESET
                continue
