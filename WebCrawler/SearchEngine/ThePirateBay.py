# coding:utf-8
from .__init__ import SearchEngine
from WebCrawler.SearchResult.MagnetResult import MagnetResult
from WebCrawler.SearchResult.VideoResult import VideoResult

import urllib.request, urllib.error, urllib.parse

RED = '\033[31m'
BLUE = '\033[4;;34m'
RESET = '\033[0m'


class ThePirateBayResult(MagnetResult, VideoResult):
    @classmethod
    def set(cls):
        pass

    def rate(self):
        mr = self.PIRATE_BAY_RESULT_SETTINGS['magnet'] * MagnetResult.rate(self)
        vr = self.PIRATE_BAY_RESULT_SETTINGS['video'] * VideoResult.rate(self)
        return mr + vr

    def __str__(self):
        string = '# ' + self.name + '\n'
        string += '# Type: ' + self.type
        string += '   SE: ' + str(self.num_seeder)
        string += '   LE: ' + str(self.num_leecher) + '\n\n'
        string += BLUE + self.link + RESET + '\n\n'
        string += '# Upload time: ' + self.time
        string += '   Size: ' + self.size
        string += '   Uploader: ' + self.uploader + '\n'
        return string


ThePirateBayResult.load()


class ThePirateBay(SearchEngine):
    def generate_url(self, page=0):
        head = 'https://thepiratebay.cd/search/'
        tail = '/' + str(page) + '/7//'
        return head + urllib.parse.quote(self.key_words) + tail

    def test(self):
        title = self.cur_page.h2.stripped_strings
        next(title)
        msg = next(title).split()
        return msg[0] != 'No'

    def results_in_page(self):
        for result_msg in self.cur_page.find(id='searchResult').tbody('tr'):
            type_msg = result_msg.select('td > center > a')
            msg_iter = result_msg.select('td > font')[0].stripped_strings
            msg = next(msg_iter).split(',')
            number = result_msg.select('td[align]')
            yield ThePirateBayResult({
                'type': type_msg[0].string + ' ' + type_msg[1].string,
                'name': result_msg.select('td > div')[0].a.string,
                'link': result_msg.select('td > a')[0]['href'],
                'time': msg[0][9:],
                'size': msg[1][6:],
                'uploader': next(msg_iter),
                'num_seeder': int(number[0].string),
                'num_leecher': int(number[1].string)
            })


ThePirateBay.set({'thepiratebay.cd': 5}, 10)
