import sys
import abc

from ..Tools.WebPageGrabber import WebPageGrabber


class SearchError(Exception):
    pass


class WebError(SearchError):
    pass


class ExtractError(SearchError):
    def __init__(self, e):
        self.e = e

    def __str__(self):
        return str(self.e)


# TODO needs a better way than returning None while countering web failure (also including 'unwrap')

# a super class of search engines
# you may need to modify the time limit between each grabbing action which has a default value one minute
class SearchEngine(metaclass=abc.ABCMeta):
    __WPG = None

    def __init_subclass__(cls, site_settings=None, **kwargs):
        super(SearchEngine, cls).__init_subclass__(**kwargs)
        if site_settings is not None:
            cls.__WPG = WebPageGrabber(**site_settings)
        else:
            cls.__WPG = WebPageGrabber()

    @classmethod
    def _html_parse(cls, url):
        return cls.__WPG.html_parse(url)

    # you may need to modify some of the values
    def __init__(self):
        # this member stores the current key word
        self.key_words = ''
        self.results_num = 0
        # this member stores current page index
        self._cur_page_num = 0
        # this member stores 'BeautifulSoup' object of current page
        self._cur_page = None

    # reset
    def _reset(self):
        self.key_words = ''
        self._cur_page_num = 0
        self.results_num = 0
        self._cur_page = None

    # you need to override this function to return the correct url
    @abc.abstractmethod
    def _generate_url(self, page=0):
        raise NotImplementedError

    # this function carries out grabbing action
    def _mod_current_page(self, page=0):
        self._cur_page = self._html_parse(self._generate_url(page))
        self._cur_page_num = page
        return self._cur_page is not None

    # set a new key word
    def search(self, key_words):
        self._reset()
        self.key_words = key_words
        self.results_num = self._get_results_num() if self._mod_current_page() else -1
        return self.results_num

    @abc.abstractmethod
    def _get_results_num(self):
        raise NotImplementedError

    # test whether there is result
    # you need to override it
    @abc.abstractmethod
    def _test(self):
        raise NotImplementedError

    # return an iterator of results in one page
    # you need to override it
    @abc.abstractmethod
    def _results_in_page(self):
        raise NotImplementedError

    # return an iterator of results
    def results(self):
        try:
            if self.results_num > 0:
                yield from self._results_in_page()
            while self._test() and self._mod_current_page(self._cur_page_num + 1):
                yield from self._results_in_page()
        except Exception as e:
            # TODO should improve
            bt = sys.exc_info()[2]
            raise ExtractError(e).with_traceback(bt)

    @staticmethod
    def url_parse(url):
        return WebPageGrabber.url_parse(url)

    @staticmethod
    def unwrap(fn):
        try:
            return fn()
        except (IndexError, AttributeError, TypeError):
            pass
