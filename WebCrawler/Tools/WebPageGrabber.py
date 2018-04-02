# coding:utf-8
import httplib, urllib, urllib2, socket, time, re, threading
import requests
from bs4 import BeautifulSoup

# avoid chunked
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

# set default time to 30 sec
socket.setdefaulttimeout(30)

# beta 0
# this version is not completed and will probably be modified in near future

RED = '\033[31m'
BLUE = '\033[4;;34m'
RESET = '\033[0m'

# chrome headers
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/63.0.3239.132 Safari/537.36'}


class WebPageGrabber:
    WPG = {}
    DOMAIN = re.compile('http[s]?://([\w.]*?)/')
    LOCK = threading.Lock()

    @classmethod
    def get(cls, name='default'):
        cls.LOCK.acquire()
        if name not in cls.WPG:
            cls.WPG[name] = cls()
        cls.LOCK.release()
        return cls.WPG[name]

    def __init__(self):
        # time limit of each site
        self.sites = {}
        self.timeout = 60

    # modify the time limit
    def mod_site(self, site, limit=60):
        self.LOCK.acquire()
        if site not in self.sites:
            self.sites[site] = [limit, time.time()]
        else:
            self.sites[site][0] = limit
        self.LOCK.release()

    # get time limit information
    def get_site(self, site):
        self.LOCK.acquire()
        if site not in self.sites:
            self.sites[site] = [60, time.time()]
        wait_time = self.sites[site][1] - time.time()
        self.sites[site][1] += self.sites[site][0]
        self.LOCK.release()
        return max(0, wait_time)

    def grab_page(self, url, num_retries=2):
        # ensure the time limit between two grabbing action
        site = self.DOMAIN.findall(url)[0]
        wait_time = self.get_site(site)
        time.sleep(wait_time)
        # start grabbing web page
        print 'Grabbing web page: ' + BLUE + url + RESET
        request = urllib2.Request(url, headers=HEADERS)
        try:
            return urllib2.urlopen(request, timeout=self.timeout)
        except urllib2.HTTPError as e:
            print RED + 'Opening ' + BLUE + url + RED + ':', e, RESET
            # retry while encountered server-end error
            if num_retries > 0 and (e.code >= 500):
                return self.grab_page(url, num_retries - 1)
            else:
                return None
        except socket.error as e:
            print RED + 'Opening ' + BLUE + url + RED, e, RESET
            if num_retries > 0:
                return self.grab_page(url, num_retries - 1)
            else:
                return None
        except urllib2.URLError as e:
            print RED + 'Can\'t open ' + BLUE + url + RED + ':', e, RESET
            return None

    def parse_page(self, url, mod='html5lib', num_retries=2, lock=None):
        response = self.grab_page(url, num_retries)
        try:
            return BeautifulSoup(response, mod)
        except Exception as e:
            print RED + 'Parsing ' + BLUE + url + RED, e, RESET
            if num_retries > 0:
                return self.parse_page(url, mod, num_retries - 1)

    def download(self, url, file_name, num_retries=2):
        print 'Downloading ' + BLUE + url + RESET
        try:
            urllib.urlretrieve(url, file_name)
        except socket.timeout as e:
            print RED + 'Downloading ' + BLUE + url + RED, e, RESET
            if num_retries > 0:
                return self.download(url, file_name,  num_retries - 1)
            else:
                return None
