# coding:utf-8
import urllib2

from SearchEngine import SearchEngine
from SearchResult.SubtitleResult import SubtitleResult

BLUE = '\033[4;;34m'
RESET = '\033[0m'


class ZiMuKuResult(SubtitleResult):
    pass


class ZiMuKu(SearchEngine):
    def __init__(self):
        SearchEngine.__init__(self)
        self.grabber.mod_site(self.__class__.__name__, 5)
        self.grabber.timeout = 10
        self.num_retries = 5

    def generate_url(self, page=0):
        head = 'http://www.zimuku.cn/search?q='
        tail = '&p='
        return head + urllib2.quote(self.key_word) + tail + str(page + 1)

    def get_num(self):
        return

    def test(self):
        return len(self.cur_page.select('div.box.clearfix > p')) == 0

    def results(self):
        while True:
            for each in self.cur_page.select('div.item.prel.clearfix'):
                item = each.select('div.title')[0]
                msg_video_name = item.select('p')
                video_name_1 = msg_video_name[0].select('a > b')[0].string
                video_name_2 = msg_video_name[1].select('a')[0].string
                if video_name_1 is None:
                    video_name_1 = ''
                if video_name_2 is None:
                    video_name_2 = ''
                tr_items = item.select('tr')
                if tr_items[-1]['class'][0] == 'msub':
                    more_page = self.html_parse('http://www.zimuku.cn' + tr_items[-1].select('a')[0]['href'])
                    tr_items = more_page.find(id='subtb').select('tbody > tr')
                for tr_item in tr_items:
                    title = tr_item.select('td.first')[0]
                    detail_page = self.html_parse('http://www.zimuku.cn' + title.select('a')[0]['href'])
                    msg_detail = detail_page.select('ul.subinfo.clearfix > li')
                    lang = ''
                    for msg_lang in msg_detail[0].select('img'):
                        lang += msg_lang['alt']
                    msg_format = msg_detail[1].select('span')
                    file_format = ''
                    for span in msg_format:
                        file_format += span.string
                    num_iter = msg_detail[2].stripped_strings
                    num_iter.next()
                    time_iter = msg_detail[6].stripped_strings
                    time_iter.next()
                    try:
                        num_download = int(num_iter.next())
                    except ValueError:
                        num_download = 0
                    download_page = self.html_parse('http:' + msg_detail[-1].select('div.clearfix > a')[0]['href'])
                    ref_link = download_page.select('div.down.clearfix a')[0]['href']
                    yield ZiMuKuResult(
                        name=title.select('a > b')[0].string,
                        video_name=video_name_1 + video_name_2,
                        num_download=num_download,
                        format=file_format,
                        language=lang,
                        authour=msg_detail[5].select('span')[0].string,
                        time=time_iter.next()[:16],
                        link='http://www.subku.net' + ref_link
                    )
            self.mod_current_page(self.cur_num_page + 1)
            if len(self.cur_page.select('div.pagination.r.clearfix > div > a.next')) == 0:
                break
