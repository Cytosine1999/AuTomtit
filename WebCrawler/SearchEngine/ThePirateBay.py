from . import SearchEngine
from ..SearchResult import SearchResult, SearchResultItem
from ..SearchResult.MagnetResult import MagnetResult
from ..SearchResult.VideoResult import VideoResult


class ThePirateBayResult(SearchResult, extends=(MagnetResult, VideoResult)):
    type = SearchResultItem()
    name = SearchResultItem()
    link = SearchResultItem()
    time = SearchResultItem()
    size = SearchResultItem()
    uploader = SearchResultItem()
    num_seeder = SearchResultItem()
    num_leecher = SearchResultItem()

    def __str__(self):
        string = '# ' + self.name + '\n'
        string += '# Type: ' + self.type
        string += '   SE: ' + str(self.num_seeder)
        string += '   LE: ' + str(self.num_leecher) + '\n\n'
        string += self.link + '\n\n'
        string += '# Upload time: ' + self.time
        string += '   Size: ' + self.size
        string += '   Uploader: ' + self.uploader + '\n'
        return string


class ThePirateBay(SearchEngine, site_settings={'default': {'num_retries': 5}}):
    def _generate_url(self, page=0):
        head = 'https://thepiratebay.cd/search/'
        tail = '/' + str(page) + '/7//'
        return head + self.url_parse(self.key_words) + tail

    def _get_results_num(self):
        title = self._cur_page.h2.stripped_strings
        next(title)
        msg = next(title).split()
        return 0 if msg[0] == 'No' else int(msg[7])

    def _test(self):
        return self._cur_page_num * 30 <= self.results_num

    def _results_in_page(self):
        for result_msg in self._cur_page.find(id='searchResult').tbody('tr'):
            type_msg = result_msg.select('td > center > a')
            msg_iter = result_msg.select('td > font')[0].stripped_strings
            msg = next(msg_iter).split(',')
            number = result_msg.select('td[align]')
            yield ThePirateBayResult(
                type=type_msg[0].string + ' ' + type_msg[1].string,
                name=result_msg.select('td > div')[0].a.string,
                link=result_msg.select('td > a')[0]['href'],
                time=msg[0][9:],
                size=msg[1][6:],
                uploader=next(msg_iter),
                num_seeder=int(number[0].string),
                num_leecher=int(number[1].string)
            )
