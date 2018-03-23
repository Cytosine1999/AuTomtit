# import Settings
from SearchEngine import ExtractError
from SearchEngine.HaiDaoWan import HaiDaoWan
from SearchEngine.EZTV import EZTV
from SearchEngine.ZiMuKu import ZiMuKu
from SearchEngine.IMDb import IMDb

RED = '\033[31m'
BLUE = '\033[4;;34m'
RESET = '\033[0m'


class Sort:
    def __init__(self):
        self.top = []

    def push(self, val, obj):
        flag = False
        if len(self.top) == 0:
            self.top.append((val, obj))
        else:
            for index, each in enumerate(self.top):
                if val > each[0]:
                    self.top.insert(index, (val, obj))
                    break
            self.top.append((val, obj))
            if len(self.top) > 5:
                self.top = self.top[0:5]
        """
        print '['
        for each in self.top:
            print '    (', each[0], ',', each[1].name, ')'
        print ']'
        """


def search():
    # settings = Settings.load()
    ses = [HaiDaoWan(), EZTV(), ZiMuKu(), IMDb()]
    while True:
        print '# input 1: HaiDaoWan'
        print '# input 2: QingSongTV'
        print '# input 3: ZiMuKu'
        print '# input 4: IMDb'
        print '# input anything else to exit'
        print 'please choose which search engine you want to use:',
        num = raw_input()
        try:
            num = int(num)
        except ValueError:
            break
        except IndexError:
            break
        se = ses[num - 1]
        print 'please input key words:',
        key_word = raw_input()
        s = Sort()
        if se.search(key_word):
            try:
                for i, result in enumerate(se.results()):
                    s.push(result.rate(), result)
            except ExtractError:
                print RED + 'Can\'t parse the web page' + RESET
                continue
            for each in s.top:
                print '-' * 70
                print each[1]
            print '-' * 70
        else:
            print 'No Results!'
