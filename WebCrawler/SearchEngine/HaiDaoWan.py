# coding:utf-8
from SearchEngine import SearchEngine
from SearchResult.MagnetResult import MagnetResult
from SearchResult.VideoResult import VideoResult

import urllib2
import time

RED = '\033[31m'
BLUE = '\033[4;;34m'
RESET = '\033[0m'


def get_time(msg):
    time_msg = msg.split()
    upload_time = None
    if len(time_msg) == 4:
        if time_msg[2] == 'mins':
            upload_time = time.time() - time_msg[1] * 60
    elif len(time_msg) == 3:
        if time_msg[1] == 'today':
            localtime = time.localtime(time.time())
            year = localtime.tm_year
            mon = localtime.tm_mon
            day = localtime.tm_mday
            min = int(time_msg[0:2])
            sec = int(time_msg[2:4])
            pass
        elif time_msg[1] == 'Y-day':
            localtime = time.localtime(time.time())
            year = localtime.tm_year
            mon = localtime.tm_mon
            day = localtime.tm_mday - 1
            min = int(time_msg[0:2])
            sec = int(time_msg[2:4])
            pass
        elif time_msg[1][2] == '-':
            if time_msg[2][2] == ':':
                pass
            else:
                year = int(time_msg[2])
                if year > 1970:
                    pass
    if upload_time is None:
        print RED + 'Warning! Time format dose not match:', msg, RESET
    return upload_time


def get_size(msg):
    size_msg = msg.split()
    size_value = float(size_msg[1])
    size_unit = size_msg[2]
    size = None
    if size_unit == 'GiB':
        size = round(size_value * 1024 * 1024 * 1024)
    elif size_unit == 'MiB':
        size = round(size_value * 1024 * 1024)
    elif size_unit == 'KiB':
        size = round(size_value * 1024)
    if size is None:
        print RED + 'Warning! Size format dose not match:', msg, RESET
    return size


class HaiDaoWanResult(MagnetResult, VideoResult):
    def __str__(self):
        string = '# ' + self.name + '\n'
        string += '# Type: ' + self.type
        string += '   SE: ' + str(self.num_seeder)
        string += '   LE: ' + str(self.num_leecher) + '\n\n'
        string += BLUE + self.link + RESET + '\n\n'
        string += '# Upload time ' + self.upload_time
        string += '  Size ' + self.size
        string += '   Uploader: ' + self.uploader + '\n'
        string += '-' * 70
        return string


class HaiDaoWan(SearchEngine):
    def __init__(self):
        SearchEngine.__init__(self)
        self.grabber.mod_site(self.__class__.__name__, 10)

    def generate_url(self, page=0):
        head = 'http://thepiratebay.cd/search/'
        tail = '/' + str(page) + '/7//'
        return head + urllib2.quote(self.key_word) + tail

    def get_num(self):
        title = self.cur_page.h2.stripped_strings
        title.next()
        msg = title.next().split()
        self.num_results = int(msg[7])
        self.num_page = len(self.cur_page.find(id='content').select('> div > a'))
        if self.num_page == 0:
            self.num_page = 1

    def test(self):
        title = self.cur_page.h2.stripped_strings
        title.next()
        msg = title.next().split()
        return msg[0] != 'No'

    def results(self):
        if self.num_results <= 0:
            return
        while True:
            for result_msg in self.cur_page.find(id='main-content').tbody('tr'):
                result = {}
                type_msg = result_msg.select('td > center > a')
                result['type'] = type_msg[0].string + ', ' + type_msg[1].string
                result['name'] = result_msg.select('td > div')[0].a.string
                result['link'] = result_msg.select('td > a')[0]['href']
                msg_iter = result_msg.select('td > font')[0].stripped_strings
                msg = msg_iter.next().split(',')
                result['upload_time'] = msg[0][9:]
                result['size'] = msg[1][6:]
                result['uploader'] = msg_iter.next()
                number = result_msg.select('td[align]')
                result['num_seeder'] = int(number[0].string)
                result['num_leecher'] = int(number[1].string)
                yield HaiDaoWanResult(result)
            if not self.mod_current_page(self.cur_num_page + 1):
                break
