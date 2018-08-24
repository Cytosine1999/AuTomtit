import re
import threading
import time
import sys
import urllib

from ..Tools import WebPageGrabber


class SearchError(Exception):
    pass


class WebError(SearchError):
    pass


class ExtractError(SearchError):
    def __init__(self, e):
        self.e = e

    def __str__(self):
        return str(self.e)


# a super class of search engines
# you may need to modify the time limit between each grabbing action which has a default value one minute
class SearchEngine:
    _SITES = {
        'default': {
            'limit': 5,
            'num_retries': 2,
            'language': 'html5lib',
            'time_out': 10,
        }
    }
    _DOMAIN = re.compile('http[s]?://(?P<domain>[\w.]*?)/')
    _LOCK = threading.Lock()

    # modify the time limit
    @classmethod
    def mod_site(cls, site, **kwargs):
        lock = cls._LOCK
        if site not in cls._SITES:
            site_settings = cls._SITES['default']
            site_settings['record'] = time.time()
            site_settings.update(kwargs)
            lock.acquire()
            cls._SITES[site] = site_settings
            lock.release()
        else:
            lock.acquire()
            cls._SITES[site].update(kwargs)
            lock.release()

    # get time limit information
    @classmethod
    def get_site(cls, site):
        lock = cls._LOCK
        if site not in cls._SITES:
            site_settings = cls._SITES['default']
            site_settings['record'] = time.time()
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
        wait_time = record['record'] - time.time()
        record['record'] = time.time() + record['limit']
        lock.release()
        return max(0, wait_time)

    @classmethod
    def html_parse(cls, url):
        site = cls.get_site(cls._DOMAIN.search(url).group('domain'))
        for _ in range(site['num_retries']):
            time.sleep(cls.wait(site))
            try:
                return WebPageGrabber.parse_page(url, site['time_out'], site['language'])
            except urllib.error.URLError as e:
                sys.stderr.write('Cannot open: ' + url + ' ' + str(e) + '\n')
                return
            except urllib.error.HTTPError as e:
                sys.stderr.write('Opening: ' + url + ' ' + str(e) + '\n')
                if e.code >= 500:
                    return
                else:
                    print('Retrying...', end=' ')
            except Exception as e:
                sys.stderr.write('Parsing: ' + url + ' ' + str(e) + '\n')
                print('Retrying...', end=' ')
        print('Exceeded retries limits.')

    # you may need to modify some of the values
    def __init__(self):
        # this member stores the current key word
        self.key_words = ''
        # this member stores current page index
        self._cur_page_num = 0
        # this member stores 'BeautifulSoup' object of current page
        self._cur_page = None

    # reset
    def reset(self):
        self.key_words = ''
        self._cur_page_num = 0
        self._cur_page = None

    # you need to override this function to return the correct url
    def generate_url(self, page=0):
        raise NotImplementedError

    # this function carries out grabbing action
    def mod_current_page(self, page=0):
        self._cur_page = self.html_parse(self.generate_url(page))
        if self._cur_page is None:
            return False
        if page == 0:
            if not self.first_test():
                return False
        else:
            if not self.test():
                return False
        self._cur_page_num = page
        return True

    # set a new key word
    def search(self, key_words):
        self.reset()
        self.key_words = key_words
        return self.mod_current_page()

    # first test
    # you may need to override it
    def first_test(self):
        return self.test()

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
        # try:
        while True:
            for result in self.results_in_page():
                yield result
            if not self.mod_current_page(self._cur_page_num + 1):
                break
        # except Exception as e:
        #     raise ExtractError(e)

    @staticmethod
    def url_parse(string):
        return urllib.parse.quote(string)

    @staticmethod
    def unwrap(fn):
        try:
            return fn()
        except (IndexError, AttributeError, TypeError):
            return None
