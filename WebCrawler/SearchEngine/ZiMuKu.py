# coding:utf-8
import urllib2

from SearchEngine import SearchEngine
from SearchResult.SubtitleResult import SubtitleResult

BLUE = '\033[4;;34m'
RESET = '\033[0m'


class EZTVResult(SubtitleResult):
    pass


class EZTV(SearchEngine):
    def __init__(self):
        SearchEngine.__init__(self)
        self.grabber.mod_site(self.__class__.__name__, 10)

    def generate_url(self, page=0):
        return''

    def get_num(self):
        return

    def test(self):
        return True

    def results(self):
        while False:
            result = {}
            yield EZTVResult(result)
