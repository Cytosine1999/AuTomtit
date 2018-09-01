import sys
import copy
import re
import threading
import time
import socket
import urllib.request as url_request
import urllib.error as url_error
import urllib.parse as url_parse
import http.client as http_client
from bs4 import BeautifulSoup


# avoid chunked
http_client.HTTPConnection._http_vsn = 10
http_client.HTTPConnection._http_vsn_str = 'HTTP/1.0'


# set default time to 30 sec
socket.setdefaulttimeout(60)


# beta 0
# this version is not completed and will probably be modified in near future


# chrome headers
HEADERS = {
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'Cache-Control': 'no-cache',
    # 'Connection': 'Upgrade',
    # 'Host': 'hodling.faith.',
    # 'Pragma': 'no-cache',
    # 'Upgrade': 'websocket',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/65.0.3325.181 Safari/537.36'
}


class WebPageGrabber:
    class _SiteSettings:
        __slots__ = ('limit', 'num_retries', 'language', 'time_out', 'record')

        def __init__(self, **kwargs):
            for filed in self.__slots__:
                self.__setattr__(filed, kwargs[filed])

        def update(self, **kwargs):
            for key, value in kwargs.items():
                self.__setattr__(key, value)

    __DOMAIN = re.compile('http[s]?://(?P<domain>[\w.]*?)/')

    __slots__ = ('_sites', 'lock')

    def __init__(self, **site_settings):
        self._sites = {
                'default': self._SiteSettings(
                    limit=5,
                    num_retries=2,
                    language='html5lib',
                    time_out=10,
                    record=time.time(),
                )
            }
        self.lock = threading.Lock()
        for key, value in site_settings.items():
            self._mod_site(key, **value)

    # modify the time limit
    def _mod_site(self, site, **kwargs):
        self.lock.acquire()
        if site not in self._sites:
            self._sites[site] = copy.deepcopy(self._sites['default'])
        self._sites[site].update(**kwargs)
        self.lock.release()

    # get time limit information
    def _get_site(self, site):
        self.lock.acquire()
        if site not in self._sites:
            self._sites[site] = copy.deepcopy(self._sites['default'])
        self.lock.release()
        return self._sites[site]

    def _wait(self, record):
        self.lock.acquire()
        wait_time = record.record - time.time()
        record.record = time.time() + record.limit
        self.lock.release()
        return max(0, wait_time)

    def html_parse(self, url):
        site = self._get_site(self.__DOMAIN.search(url).group('domain'))
        for _ in range(site.num_retries):
            time.sleep(self._wait(site))
            try:
                return self.parse_page(url, site.time_out, site.language)
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

    @staticmethod
    def grab_page(url, timeout=60):
        print('Grabbing web page:', url)
        request = url_request.Request(url, headers=HEADERS)
        return url_request.urlopen(request, timeout=timeout)
        # return requests.get(url, headers={}, timeout=self.timeout, verify=False).content

    @staticmethod
    def parse_page(url, timeout=60, language='html5lib'):
        response = WebPageGrabber.grab_page(url, timeout)
        print('Parsing web page:', url)
        return BeautifulSoup(response, language)

    @staticmethod
    def download(url, file_name):
        print('Downloading:', url)
        url_request.urlretrieve(url, file_name)

    @staticmethod
    def url_parse(string):
        return url_parse.quote(string)
