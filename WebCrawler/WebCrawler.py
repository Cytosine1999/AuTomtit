# coding:utf-8
import sys
import httplib
# import urllib
# from bs4 import BeautifulSoup

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

if __name__ == '__main__':
    """
    page_num = int(soup.find(id='page').select('span.pc')[0].string)
    soup.find(id='content_left').select('div')
    """
    """
    wpg = WebPageGrabber()
    respond = wpg.grab_page('http://www.zimuku.cn/search?q=this%20is%20us')
    soup = BeautifulSoup(respond.read(), 'html5lib')
    """
    """
    urllib.urlretrieve('http://www.subku.net/download'
                       '/MTAwMjY2fGNkYjNlNjM1MmFlYWJkZjYwNzI2NzE0NHwxNTE4MjcwNDg5fDQ4N2EzZGQ0fHJlbW90ZQ%3D%3D/svr/dx1'
                       '', "demo.zip") 
    """

    while True:
        print 'please choose which search engine you want to use'
        print 'input 1: HaiDaoWan'
        print 'input 2: QingSongTV'
        print 'input 3: ZiMuKu'
        print 'input anything else to exit'
        num = raw_input()
        if num == '1':
            print 'please input key words:'
            key_word = raw_input()
            print
            se = HaiDaoWan()
        elif num == '2':
            print 'please input key words:'
            key_word = raw_input()
            print
            se = EZTV()
        elif num == '3':
            print 'please input key words:'
            key_word = raw_input()
            print
            se = ZiMuKu()
        else:
            break
        if se.search(key_word):
            print
            print '# Showing results 10 at a time'
            print '# press enter to show next 10 results'
            print '# or input \'exit\' to exit'
            print
            print '-' * 70
            for index, result in enumerate(se.results()):
                print '# Number:', (index + 1)
                print result
                if ((index + 1) % 10) == 0:
                    if raw_input() == 'exit':
                        break
        print 'No more results!'
