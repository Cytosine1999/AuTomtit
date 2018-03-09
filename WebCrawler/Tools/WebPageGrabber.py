# coding:utf-8
import urllib
import urllib2
import socket
import time
from bs4 import BeautifulSoup

# beta 0
# this version is not completed and will probably be modified in near future

RED = '\033[31m'
BLUE = '\033[4;;34m'
RESET = '\033[0m'

# chrome headers
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/63.0.3239.132 Safari/537.36'}


class WebPageGrabber:
    def __init__(self, name='default', sync=False, timeout=60):
        # the name of the crawler
        # crawler with same name will share a same time limit
        self.name = name
        # time limit information
        # synchronized with file defined in 'WebPageGrabber.conf'
        # owner 'default' is for web pages without pointing out owners
        # owner 'default' has a default limit which is as least one minute between two grabbing action
        self.sites = {'default': [60, time.time()]}
        # set whether to synchronize with file
        self.sync = sync
        self.timeout = timeout

    # add new data to the file
    def write_sites(self):
        pass

    # get new data from the file
    def read_sites(self):
        pass

    # modify the time limit
    def mod_site(self, name, limit=60, t=time.time()):
        self.sites[name] = [limit, t]
        if self.sync:
            self.write_sites()

    # get time limit information
    def get_site(self, site):
        if site not in self.sites:
            self.mod_site(site)
        if self.sync:
            self.read_sites()
        return self.sites[site]

    # grab a web page which owns to 'site' and with reties less than 'num_retries'
    def grab_page(self, url, site='default', num_retries=2):
        # ensure the time limit between two grabbing action
        site_limit = self.get_site(site)
        t = site_limit[1] - time.time()
        if t > 0:
            time.sleep(t)
        self.mod_site(site, site_limit[0], time.time() + site_limit[0])

        # start grabbing web page
        print 'Grabbing web page: ' + BLUE + url + RESET
        request = urllib2.Request(url, headers=HEADERS)
        try:
            return urllib2.urlopen(request, timeout=self.timeout)
        except urllib2.HTTPError as e:
            print RED + 'Can\'t open ' + BLUE + url + RED + ':', e, RESET
            # retry while encountered server-end error
            if num_retries > 0 and (e.code >= 500):
                return self.grab_page(url, site, num_retries - 1)
            else:
                return None
        except socket.error as e:
            print RED + 'Opening ' + BLUE + url + RED, e, RESET
            if num_retries > 0:
                return self.grab_page(url, site, num_retries - 1)
            else:
                return None
        except urllib2.URLError as e:
            print RED + 'Can\'t open ' + BLUE + url + RED + ':', e, RESET
            return None

    def parse_page(self, url, site='default', mod='html5lib', num_retries=2):
        response = self.grab_page(url, site, num_retries)
        try:
            return BeautifulSoup(response, mod)
        except Exception as e:
            print RED + 'Parsing ' + BLUE + url + RED, e, RESET
            if num_retries > 0:
                return self.parse_page(url, site, mod, num_retries - 1)

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

