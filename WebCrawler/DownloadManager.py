import os
import time
import threading

from .. import Settings
from ..Log import Log
# from .Sort import Sort
# from .SearchEngine import ExtractError
# from .SearchEngine.IMDb import IMDb
# from .SearchEngine.EZTV import EZTV
from .SearchEngine.ThePirateBay import ThePirateBay
from .SearchEngine.ZiMuKu import ZiMuKu


class Search(threading.Thread):
    def __init__(self, nm, se, kw, color):
        threading.Thread.__init__(self)
        self.se = se
        self.kw = kw
        self.log = Log(nm, color)

    def run(self):
        if self.se.search(self.kw):
            for result in self.se.results():
                self.log.msg(None, (
                    (str(result), 'default'),
                    ('-' * 70, 'default')
                ), print=True, linebreak=True)
        self.log.msg(None, (
            ('terminated', self.log.color)
        ), print=True)

    def status(self):
        pass


class Transmission(threading.Thread):
    def __init__(self, path, torrents, sleep_time):
        threading.Thread.__init__(self)
        self.path = path
        self.torrents = torrents
        self.sleep_time = sleep_time

    # keep transmission downloading
    def run(self):
        flag = 0

        self.torrents[0].download(self.path)
        self.torrents[0].torrent.start()

        while True:
            self.torrents[flag].torrent.update()  # need this to update data
            eta = self.torrents[flag].torrent.eta
            if self.torrents[flag].torrent.status == '':
                self.torrents[flag].torrent.stop()
                flag += 1
                if flag < len(self.torrents):
                    self.torrents[flag].torrent.start()
            time.sleep(self.sleep_time)

    def status(self):
        pass


class VideoObject:
    def __init__(self):
        pass


class Sort:
    def __init__(self, size):
        self.size = size
        self.top = []

    def get_top(self):
        return self.top[0][1]

    def push(self, val, obj):
        if len(self.top) == 0:
            self.top.append((val, obj))
        else:
            for index, each in enumerate(self.top):
                if val > each[0]:
                    self.top.insert(index, (val, obj))
                    break
            self.top.append((val, obj))
            if len(self.top) > self.size:
                self.top = self.top[0:self.size]

    def get_tops(self):
        return list(map(lambda x: x[1], self.top))


def run():
    tpb = Search('thepiratebay', ThePirateBay(), 'doctor who', 'green')
    zmk = Search('zimuku', ZiMuKu(), 'doctor who', 'yellow')

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


# the main thread keep watching at other threads
def run_():
    settings = Settings.load()
    download_path = settings['download path']
    key_words = input('Please enter key words:')
    pirate_bay = ThePirateBay()
    path = download_path + '/' + key_words
    if not os.path.exists(path):
        os.makedirs(path)
    s = Sort(5)
    if pirate_bay.search(key_words):
        for result in pirate_bay.results():
            s.push(result.rate(), result)
        transmission = Transmission(path, s.get_tops(), 60)
        transmission.start()
        transmission.join()
