# coding:utf-8
from SearchEngine.HaiDaoWan import HaiDaoWan
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

    print 'please input key words:'
    key_word = raw_input()
    print
    se = HaiDaoWan()
    nr = se.search(key_word)
    print
    print '# Have', nr, 'results'
    print '# Showing results 10 at a time'
    print '# press enter to show next 10 results'
    print
    print '-' * 70
    for index, result in enumerate(se.results()):
        print '# Number:', (index + 1)
        print result
        if ((index + 1) % 10) == 0:
            raw_input()
    print 'No more results!'
