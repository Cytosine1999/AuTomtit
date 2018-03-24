import urllib2

from __init__ import SearchEngine
from WebCrawler.SearchResult import SearchResult


class IMDbResult(SearchResult):
    pass


class IMDb(SearchEngine):
    def __init__(self):
        SearchEngine.__init__(self)
        self.grabber.mod_site(self.__class__.__name__, 5)
        self.grabber.timeout = 10

    def generate_url(self, page=0):
        head = 'http://www.imdb.com/find?ref_=nv_sr_fn&q='
        tail = '&s=tt'
        return head + urllib2.quote(self.key_word) + tail

    def first_test(self):
        return True

    def test(self):
        return False

    def results_in_page(self):
        for result in self.cur_page.select('table.findList')[0].select('tr'):
            path = result.select('td')[1].a['href']
            detail_page = self.html_parse('http://www.imdb.com' + path)
            over_view = detail_page.find(id='title-overview-widget')
            title_parent = self.unwrap(over_view, lambda a: a.select('div.titleParent')[0])
            title_bar = over_view.select('div.title_bar,.titleBar')[0]
            ratings_wrapper = self.unwrap(over_view, lambda a: a.select('div.ratings_wrapper')[0])
            sub_text = self.unwrap(title_bar, lambda a: a.select('div.subtext')[0])
            yield IMDbResult(
                name=self.un_strings(title_bar.select('h1')[0].stripped_strings),
                parent_name=self.unwrap(title_parent, lambda a: a.a.string),
                parent_time=self.unwrap(title_parent, lambda a: a.span.string),
                rate=self.unwrap(ratings_wrapper, lambda a: a.select('strong > span')[0].string),
                duration=self.unwrap(sub_text, lambda a: a.select('time')[0].string.strip()),
                type=self.unwrap(sub_text, lambda a: self.un_list(a.select('span.itemprop')))
            )

    @staticmethod
    def un_strings(strings):
        string = ''
        for each in strings:
            string += each + ' '
        return string

    @staticmethod
    def un_list(obj):
        string = ''
        for each in obj:
            string += each.string + ' '
        return string
