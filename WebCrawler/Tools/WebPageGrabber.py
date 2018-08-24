import http
import urllib
import socket
from bs4 import BeautifulSoup

# avoid chunked
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

# set default time to 30 sec
socket.setdefaulttimeout(30)

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


def grab_page(url, timeout=60):
    print('Grabbing web page:', url)
    request = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(request, timeout=timeout)
    # return requests.get(url, headers={}, timeout=self.timeout, verify=False).content


def parse_page(url, timeout=60, language='html5lib'):
    print('Parsing web page:', url)
    response = grab_page(url, timeout)
    return BeautifulSoup(response, language)


def download(url, file_name):
    print('Downloading:', url)
    urllib.request.urlretrieve(url, file_name)
