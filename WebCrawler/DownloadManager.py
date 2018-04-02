import os
import threading

import Settings
# from Sort import Sort
from WebCrawler.SearchEngine import ExtractError
# from SearchEngine.IMDb import IMDb
from WebCrawler.SearchEngine.EZTV import EZTV
from WebCrawler.SearchEngine.ThePirateBay import ThePirateBay
from WebCrawler.SearchEngine.ZiMuKu import ZiMuKu

RED = '\033[31m'
BLUE = '\033[4;;34m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RESET = '\033[0m'


class Search(threading.Thread):
    LOCK = threading.Lock()

    def __init__(self, nm, se, kw, color):
        threading.Thread.__init__(self)
        self.nm = nm
        self.se = se
        self.kw = kw
        self.color = color

    def run(self):
        if self.se.search(self.kw):
            for result in self.se.results():
                self.LOCK.acquire()
                print(self.color + '$ thread', self.nm, RESET)
                print(result.name)
                self.LOCK.release()
        self.LOCK.acquire()
        print(self.color + '$ thread', self.nm, 'terminated' + RESET)
        self.LOCK.release()


def run():
    tpb = Search('thepiratebay', ThePirateBay(), 'doctor who', GREEN)
    zmk = Search('zimuku', ZiMuKu(), 'doctor who', YELLOW)

    tpb.start()
    zmk.start()
    tpb.join()
    zmk.join()

    """
    settings = Settings.load()
    download_path = settings['download path']
    print 'Please enter key words:',
    key_words = raw_input()
    imdb = IMDb()
    imdb.details = True
    pirate_bay = PirateBay()
    if imdb.search(key_words):
        path = download_path + '/' + key_words
        info = imdb.result()
        info.download_poster(path)
        if not os.path.exists(path):
            os.makedirs(path)
        info_file = file(path + '/' + key_words + '.txt', 'w')
        info_file.write(str(info))
        s = Sort(1)
        if pirate_bay.search(key_words):
            try:
                for result in pirate_bay.results():
                    s.push(result.rate(), result)
            except ExtractError:
                print RED + 'Can\'t parse the web page' + RESET
        s.get_top().download()
    else:
        print 'Can\'t find \"' + key_words + '\"'
    """
