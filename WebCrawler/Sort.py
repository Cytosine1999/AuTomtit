# import Settings
from .SearchEngine import ExtractError
from .SearchEngine.ThePirateBay import ThePirateBay
from .SearchEngine.EZTV import EZTV
from .SearchEngine.ZiMuKu import ZiMuKu
from .SearchEngine.IMDb import IMDb

RED = '\033[31m'
BLUE = '\033[4;;34m'
RESET = '\033[0m'


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
                self.top = self.top[0:5]


def run():
    # settings = Settings.load()
    ses = [ThePirateBay(), EZTV(), ZiMuKu(), IMDb()]
    while True:
        print('# input 1: HaiDaoWan')
        print('# input 2: QingSongTV')
        print('# input 3: ZiMuKu')
        print('# input 4: IMDb')
        print('# input anything else to exit')
        print('please choose which search engine you want to use:', end=' ')
        num = input()
        try:
            num = int(num)
        except ValueError:
            break
        except IndexError:
            break
        se = ses[num - 1]
        print('please input key words:', end=' ')
        key_word = input()
        s = Sort(5)
        if se.search(key_word):
            try:
                for i, result in enumerate(se.results()):
                    s.push(result.rate(), result)
            except ExtractError:
                print(RED + 'Can\'t parse the web page' + RESET)
                continue
            for each in s.top:
                print('-' * 70)
                print(each[1])
            print('-' * 70)
        else:
            print('No Results!')
