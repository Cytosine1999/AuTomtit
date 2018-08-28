# coding:utf-8
from . import SearchEngine
from ..SearchResult.HTTPResult import HTTPResult


class BaiduResult(HTTPResult):
    pass


class Baidu(SearchEngine):
    def generate_url(self, page=0):
        head = 'https://baidu/s?wd='
        tail = '&pn='
        return head + self.url_parse(self.key_words) + tail + str(page * 10)

    def test(self):
        footer = self._cur_page.find(id='page').select('span.pc')
        if len(footer) > 0:
            pass
        else:
            pass
        return False

    def results_in_page(self):
        for result in self._cur_page.find(id='content_left').select('div'):
            title_msg = result.select('h3.t')[0]
            # description_msg = result.select('div.c-abstract')[0]
            # source_msg = result.select('div.f13')[0]
            yield BaiduResult({
                'name': title_msg.a.string,
                'link': title_msg.a['href']
            })
