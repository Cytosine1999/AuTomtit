# coding:utf-8
from .__init__ import SearchEngine
from ..SearchResult.SubtitleResult import SubtitleResult


BLUE = '\033[4;;34m'
RESET = '\033[0m'


class ZiMuKuResult(SubtitleResult):
    pass


class ZiMuKu(SearchEngine):
    DOMAIN_BASE = 'https://www.zimuku.cn'
    DOMAIN_DOWNLOAD = 'https://www.subku.net'

    def generate_url(self, page=0):
        head = 'https://www.zimuku.cn/search?q='
        tail = '&p='
        return head + self.url_parse(self.key_words) + tail + str(page + 1)

    def first_test(self):
        return len(self._cur_page.select('div.box.clearfix > p')) == 0

    def test(self):
        return len(self._cur_page.select('div.pagination.r.clearfix > div > a.next')) == 0

    def results_in_page(self):
        for each in self._cur_page.select('div.item.prel.clearfix'):
            item = each.select('div.title')[0]
            msg_video_name = item.select('p')
            video_name_1 = msg_video_name[0].a.b.string
            video_name_2 = msg_video_name[1].a.string
            if video_name_1 is None:
                video_name_1 = ''
            if video_name_2 is None:
                video_name_2 = ''
            tr_items = item.select('tr')
            if tr_items[-1]['class'][0] == 'msub':
                more_page = self.html_parse(self.DOMAIN_BASE + tr_items[-1].a['href'])
                tr_items = more_page.find(id='subtb').select('tbody > tr')
            for tr_item in tr_items:
                title = tr_item.select('td.first')[0]
                detail_page = self.html_parse(self.DOMAIN_BASE + title.a['href'])
                msg_detail = detail_page.select('ul.subinfo.clearfix > li')
                lang = ''
                for msg_lang in msg_detail[0].select('img'):
                    lang += msg_lang['alt']
                msg_format = msg_detail[1].select('span')
                file_format = ''
                for span in msg_format:
                    file_format += span.string
                num_iter = msg_detail[2].stripped_strings
                next(num_iter)
                time_iter = msg_detail[6].stripped_strings
                next(time_iter)
                try:
                    num_download = int(next(num_iter))
                except ValueError:
                    num_download = 0
                download_page = self.html_parse(msg_detail[-1].select('div.clearfix > a')[0]['href'])
                ref_link = download_page.select('div.down.clearfix a')[0]['href']
                yield ZiMuKuResult({
                    'name': title.a.b.string,
                    'video_name': video_name_1 + video_name_2,
                    'num_download': num_download,
                    'format': file_format,
                    'language': lang,
                    'author': msg_detail[5].span.string,
                    'time': next(time_iter)[:16],
                    'link': ref_link
                })


ZiMuKu.mod_site('default', num_retries=5)
