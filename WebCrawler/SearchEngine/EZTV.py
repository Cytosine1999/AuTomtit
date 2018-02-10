from SearchEngine import SearchEngine
from SearchResult.SearchResult import SearchResult


class EZTVResult(SearchResult):
    pass


class EZTV(SearchEngine):
    def __init__(self):
        SearchEngine.__init__(self)
        self.grabber.mod_site(self.__class__.__name__, 10)

    def generate_url(self, page=0):
        pass

    def get_num(self):
        pass

    def test(self):
        return False

    def results(self):
        while False:
            yield None
