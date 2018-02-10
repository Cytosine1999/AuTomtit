# coding:utf-8
from SearchEngine.HaiDaoWan import HaiDaoWan
from SearchEngine.EZTV import EZTV
# from SearchResult.SearchResult import SearchResult
# from WebPageGrabber import WebPageGrabber
# from bs4 import BeautifulSoup
# from data import soup

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    """
    page_num = int(soup.find(id='page').select('span.pc')[0].string)
    soup.find(id='content_left').select('div')
    """
    """
    wpg = WebPageGrabber()
    respond = wpg.grab_page('https://www.baidu.com/s?wd=1&pn=800')
    print respond.read()
    """

    while True:
        print 'please choose which search engine you want to use'
        print 'input 1: HaiDaoWan'
        print 'input 2: QingSongTV'
        print 'input exit to exit'
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
                    if raw_input() == 'next':
                        continue
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
                    if raw_input() == 'next':
                        continue
            print 'No more results!'
        elif num == 'next':
            break
        else:
            print 'input denied'
