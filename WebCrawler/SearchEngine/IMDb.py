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

    def test(self):
        return True

    def results_in_page(self):
        for result in self.cur_page.select('table.findList')[0].select('tr'):
            path = result.select('td')[1].a['href']
            detail_page = self.html_parse('http://www.imdb.com' + path)
            # main = detail_page.fild(id='content-2-wide')
            over_view = detail_page.find(id='title-overview-widget')
            title = over_view.select('h1')[0].strings.next() # TODO inf title
            if len(over_view.select('div.notEnoughRatings')) == 0:
                rate = over_view.select('div.ratingValue span')[0].string
            else:
                rate = 'No enough ratings'
            yield IMDbResult(
                name=title,
                rate=rate
            )
