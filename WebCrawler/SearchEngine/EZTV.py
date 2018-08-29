# coding:utf-8
from . import SearchEngine
from ..SearchResult.MagnetResult import MagnetResult
from ..SearchResult.VideoResult import VideoResult


class EZTVResult(MagnetResult, VideoResult):
    __slots__ = ('name', 'link', 'size', 'time', 'num_seeder')

    def __str__(self):
        string = '# ' + self.name + '\n\n'
        string += self.link + '\n\n'
        string += '# Upload time: ' + self.time
        string += '  Size: ' + self.size
        string += '   SE: ' + str(self.num_seeder) + '\n'
        return string


class EZTV(SearchEngine):
    def generate_url(self, page=0):
        head = 'https://eztv.ag/search/'
        return head + self.url_parse(self.key_words)

    def get_results_num(self):
        return len(self._cur_page.select('tr.forum_header_border'))

    def test(self):
        return False

    def results_in_page(self):
        for tr_element in self._cur_page.select('tr.forum_header_border'):
            tds = tr_element.select('td.forum_thread_post')
            yield EZTVResult(
                name=tds[1].a.string,
                link=tds[2].a['href'],
                size=tds[3].string,
                time=tds[4].string,
                num_seeder=tds[5].string
            )
