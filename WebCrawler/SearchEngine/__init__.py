import re
import sys
import threading
import time
import urllib.error as url_error
import urllib.parse as url_parse
import copy

from ..Tools import WebPageGrabber


class SearchError(Exception):
    pass


class WebError(SearchError):
    pass


class ExtractError(SearchError):
    def __init__(self, e, html):
        self.e = e
        self.html = html

    def __str__(self):
        return str(self.e) + '\n' * 2 + str(self.html)


# a super class of search engines
# you may need to modify the time limit between each grabbing action which has a default value one minute
class SearchEngine:
    class _SiteSettings:
        __slots__ = ('limit', 'num_retries', 'language', 'time_out', 'record')

        def __init__(self, **kwargs):
            for filed in self.__slots__:
                self.__setattr__(filed, kwargs[filed])

        def to_dict(self):
            dictionary = {}
            for filed in self.__slots__:
                dictionary[filed] = self.__getattribute__(filed)
            return dictionary

        def update(self, **kwargs):
            for key, value in kwargs.items():
                self.__setattr__(key, value)

        def __repr__(self):
            return str(self.to_dict())

    _DOMAIN = re.compile('http[s]?://(?P<domain>[\w.]*?)/')
    _LOCK = threading.Lock()
    _SITES = {
        'default': _SiteSettings(
            limit=5,
            num_retries=2,
            language='html5lib',
            time_out=10,
            record=time.time(),
        )
    }

    def __init_subclass__(cls, site_settings=None, new_slots=None, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._SITES = copy.deepcopy(SearchEngine._SITES)
        cls._LOCK = threading.Lock()
        if site_settings is not None:
            for key, value in site_settings.items():
                cls.mod_site(key, **value)
        if new_slots is not None:
            cls.__slots__ = SearchEngine.__slots__ + new_slots
        else:
            cls.__slots__ = SearchEngine.__slots__

    # modify the time limit
    @classmethod
    def mod_site(cls, site, **kwargs):
        lock = cls._LOCK
        if site not in cls._SITES:
            site_settings = copy.deepcopy(cls._SITES['default'])
            site_settings.update(**kwargs)
            lock.acquire()
            cls._SITES[site] = site_settings
            lock.release()
        else:
            lock.acquire()
            cls._SITES[site].update(**kwargs)
            lock.release()

    # get time limit information
    @classmethod
    def get_site(cls, site):
        lock = cls._LOCK
        if site not in cls._SITES:
            site_settings = copy.deepcopy(cls._SITES['default'])
            lock.acquire()
            cls._SITES[site] = site_settings
            lock.release()
        else:
            site_settings = cls._SITES[site]
        return site_settings

    @classmethod
    def wait(cls, record):
        lock = cls._LOCK
        lock.acquire()
        wait_time = record.record - time.time()
        record.record = time.time() + record.limit
        lock.release()
        return max(0, wait_time)

    @classmethod
    def html_parse(cls, url):
        site = cls.get_site(cls._DOMAIN.search(url).group('domain'))
        for _ in range(site.num_retries):
            time.sleep(cls.wait(site))
            try:
                return WebPageGrabber.parse_page(url, site.time_out, site.language)
            except url_error.HTTPError as e:
                sys.stderr.write('Opening: ' + url + ' ' + str(e) + '\n')
                if e.code >= 500:
                    return None
            except url_error.URLError as e:
                sys.stderr.write('Cannot open: ' + url + ' ' + str(e) + '\n')
                return None
            except Exception as e:
                sys.stderr.write('Parsing: ' + url + ' ' + str(e) + '\n')
            print('Retrying...', end=' ')
        print('Exceeded retries limits.')

    __slots__ = ('key_words', 'results_num', '_cur_page_num', '_cur_page')

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
    def reset(self):
        self.key_words = ''
        self._cur_page_num = 0
        self.results_num = 0
        self._cur_page = None

    # you need to override this function to return the correct url
    def generate_url(self, page=0):
        raise NotImplementedError

    # this function carries out grabbing action
    def mod_current_page(self, page=0):
        self._cur_page = self.html_parse(self.generate_url(page))
        self._cur_page_num = page
        return self._cur_page is not None

    # set a new key word
    def search(self, key_words):
        self.reset()
        self.key_words = key_words
        self.results_num = self.get_results_num() if self.mod_current_page() else 0
        return self.results_num

    def get_results_num(self):
        raise NotImplementedError

    # test whether there is result
    # you need to override it
    def test(self):
        raise NotImplementedError

    # return an iterator of results in one page
    # you need to override it
    def results_in_page(self):
        raise NotImplementedError

    # return an iterator of results
    def results(self):
        try:
            if self.results_num > 0:
                for result in self.results_in_page():
                    yield result
            while self.test() and self.mod_current_page(self._cur_page_num + 1):
                for result in self.results_in_page():
                    yield result
        except Exception as e:
            raise ExtractError(e, self._cur_page)

    @staticmethod
    def url_parse(string):
        return url_parse.quote(string)

    @staticmethod
    def unwrap(fn):
        try:
            return fn()
        except (IndexError, AttributeError, TypeError):
            return None
