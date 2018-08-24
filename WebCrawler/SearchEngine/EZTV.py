# coding:utf-8
from .__init__ import SearchEngine
from ..SearchResult.MagnetResult import MagnetResult
from ..SearchResult.VideoResult import VideoResult

BLUE = '\033[4;;34m'
RESET = '\033[0m'


class EZTVResult(MagnetResult, VideoResult):
    def __str__(self):
        string = '# ' + self.name + '\n\n'
        string += BLUE + self.link + RESET + '\n\n'
        string += '# Upload time: ' + self.time
        string += '  Size: ' + self.size
        string += '   SE: ' + str(self.num_seeder) + '\n'
        return string


class EZTV(SearchEngine):
    def generate_url(self, page=0):
        head = 'https://eztv.ag/search/'
        return head + self.url_parse(self.key_words)

    def first_test(self):
        return True

    def test(self):
        return False

    def results_in_page(self):
        for tr_element in self._cur_page.select('tr.forum_header_border'):
            tds = tr_element.select('td.forum_thread_post')
            yield EZTVResult({
                'name': tds[1].a.string,
                'link': tds[2].a['href'],
                'size': tds[3].string,
                'time': tds[4].string,
                'num_seeder': tds[5].string
            })
