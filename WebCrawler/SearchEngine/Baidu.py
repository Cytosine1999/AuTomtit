# coding:utf-8
import urllib2

from SearchEngine import SearchEngine
from SearchResult.SearchResult import SearchResult


class BaiduResult(SearchResult):
    pass


class Baidu(SearchEngine):
    def __init__(self):
        SearchEngine.__init__(self)
        self.grabber.mod_site(self.__class__.__name__, 10)

    def generate_url(self, page=0):
        head = 'http://baidu/s?wd='
        tail = '&pn='
        return head + urllib2.quote(self.key_word) + tail + str(page * 10)

    def get_num(self):
        self.num_page = 76  # !!!!

    def test(self):
        footer = self.cur_page.find(id='page').select('span.pc')
        if len(footer) > 0:
            page_num = int(footer[0].string)
        else:
            pass
        return False

    def results(self):
        if self.num_results <= 0:
            return
        while True:
            for result in self.cur_page.find(id='content_left').select('div'):
                yield BaiduResult()
                if not self.mod_current_page(self.cur_num_page + 1):
                    break
