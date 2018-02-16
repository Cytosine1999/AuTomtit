# coding:utf-8
import urllib2

from SearchEngine import SearchEngine, ExtractError
from SearchResult.HTTPResult import HTTPResult


class BaiduResult(HTTPResult):
    pass


class Baidu(SearchEngine):
    def __init__(self):
        SearchEngine.__init__(self)
        self.grabber.mod_site(self.__class__.__name__, 10)

    def generate_url(self, page=0):
        head = 'http://baidu/s?wd='
        tail = '&pn='
        return head + urllib2.quote(self.key_word) + tail + str(page * 10)

    def test(self):
        footer = self.cur_page.find(id='page').select('span.pc')
        if len(footer) > 0:
            pass
        else:
            pass
        return False

    def results(self):
        try:
            while True:
                for result in self.cur_page.find(id='content_left').select('div'):
                    title_msg = result.select('h3.t')[0]
                    # description_msg = result.select('div.c-abstract')[0]
                    # source_msg = result.select('div.f13')[0]
                    yield BaiduResult(
                        name=title_msg.a.string,
                        link=title_msg.a['href']
                    )
                    if not self.mod_current_page(self.cur_num_page + 1):
                        break
        except Exception as e:
            raise ExtractError
