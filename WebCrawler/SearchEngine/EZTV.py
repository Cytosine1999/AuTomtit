# coding:utf-8
import urllib2

from SearchEngine import SearchEngine
from SearchResult.MagnetResult import MagnetResult
from SearchResult.VideoResult import VideoResult

BLUE = '\033[4;;34m'
RESET = '\033[0m'


class EZTVResult(MagnetResult, VideoResult):
    def __str__(self):
        string = '# ' + self.name + '\n'
        string += BLUE + self.link + RESET + '\n\n'
        string += '# Upload time: ' + self.time
        string += '  Size: ' + self.size
        string += '   SE: ' + str(self.num_seeder) + '\n'
        string += '-' * 70
        return string


class EZTV(SearchEngine):
    def __init__(self):
        SearchEngine.__init__(self)
        self.grabber.mod_site(self.__class__.__name__, 10)

    def generate_url(self, page=0):
        head = 'http://eztv.ag/search/'
        return head + urllib2.quote(self.key_word)

    def get_num(self):
        return

    def test(self):
        return True

    def results(self):
        for tr_element in self.cur_page.select('tr.forum_header_border'):
            tds = tr_element.select('td.forum_thread_post')
            yield EZTVResult(
                name=tds[1].select('a')[0].string,
                link=tds[2].select('a')[0]['href'],
                size=tds[3].string,
                time=tds[4].string,
                num_seeder=tds[5].string
            )
