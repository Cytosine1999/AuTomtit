# coding:utf-8
from SearchEngine import SearchEngine
from SearchResult.MagnetResult import MagnetResult
from SearchResult.VideoResult import VideoResult

import urllib2

RED = '\033[31m'
BLUE = '\033[4;;34m'
RESET = '\033[0m'


class HaiDaoWanResult(MagnetResult, VideoResult):
    def test(self):
        pass

    def rate(self):  # TODO
        mr = MagnetResult.rate(self)
        vr = VideoResult.rate(self)
        return (mr + vr) / 2

    def __str__(self):
        string = '# ' + self.name + '\n'
        string += '# Type: ' + self.type
        string += '   SE: ' + str(self.num_seeder)
        string += '   LE: ' + str(self.num_leecher) + '\n\n'
        string += BLUE + self.link + RESET + '\n\n'
        string += '# Upload time: ' + self.time
        string += '  Size: ' + self.size
        string += '   Uploader: ' + self.uploader + '\n'
        string += '-' * 70
        return string


class HaiDaoWan(SearchEngine):
    def __init__(self):
        SearchEngine.__init__(self)
        self.grabber.timeout = 10
        self.grabber.mod_site(self.__class__.__name__, 10)

    def generate_url(self, page=0):
        head = 'http://thepiratebay.cd/search/'
        tail = '/' + str(page) + '/7//'
        return head + urllib2.quote(self.key_word) + tail

    def test(self):
        title = self.cur_page.h2.stripped_strings
        title.next()
        msg = title.next().split()
        return msg[0] != 'No'

    def results_in_page(self):
        for result_msg in self.cur_page.find(id='main-content').tbody('tr'):
            type_msg = result_msg.select('td > center > a')
            msg_iter = result_msg.select('td > font')[0].stripped_strings
            msg = msg_iter.next().split(',')
            number = result_msg.select('td[align]')
            yield HaiDaoWanResult(
                type=type_msg[0].string + ' ' + type_msg[1].string,
                name=result_msg.select('td > div')[0].a.string,
                link=result_msg.select('td > a')[0]['href'],
                time=msg[0][9:],
                size=msg[1][6:],
                uploader=msg_iter.next(),
                num_seeder=int(number[0].string),
                num_leecher=int(number[1].string)
            )
