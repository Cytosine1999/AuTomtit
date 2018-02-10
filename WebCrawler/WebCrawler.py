# coding:utf-8
import sys
import httplib

from SearchEngine.HaiDaoWan import HaiDaoWan
from SearchEngine.EZTV import EZTV
from SearchEngine.ZiMuKu import ZiMuKu

# import urllib
# from SearchResult.SearchResult import SearchResult
# from WebPageGrabber import WebPageGrabber
# from bs4 import BeautifulSoup
# from data import soup

reload(sys)
sys.setdefaultencoding('utf-8')

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
    print soup.select('div.pagination.r.clearfix > div > span')[0].string.split()[1]
    # for each in soup.select('div.tbhd.clearfix'):
    #     print each
    #     print
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
            nr = se.search(key_word)
            print
            print '# Have', nr, 'results'
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
        elif num == '2':
            print 'please input key words:'
            key_word = raw_input()
            print
            se = EZTV()
            se.search(key_word)
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
        elif num == '3':
            print 'please input key words:'
            key_word = raw_input()
            print
            se = ZiMuKu()
            se.search(key_word)
            print
            print '# Showing results 10 at a time'
            print '# press enter to show next 10 results'
            print '# or input \'exit\' to exit'
            print
            print '-' * 70
            for index, result in enumerate(se.results()):
                print '# Number:', (index + 1)
                print result
                print
                if ((index + 1) % 10) == 0:
                    if raw_input() == 'exit':
                        break
            print 'No more results!'
        else:
            break
