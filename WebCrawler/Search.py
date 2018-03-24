# import Settings
from SearchEngine import ExtractError
from SearchEngine.HaiDaoWan import HaiDaoWan
from SearchEngine.EZTV import EZTV
from SearchEngine.ZiMuKu import ZiMuKu
from SearchEngine.IMDb import IMDb

RED = '\033[31m'
BLUE = '\033[4;;34m'
RESET = '\033[0m'


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
        if se.search(key_word):
            print '# Showing results 10 at a time'
            print '# press enter to show next 10 results'
            print '# or input \"exit\" to exit'
            print '-' * 70
            try:
                for i, result in enumerate(se.results()):
                    index = i + 1
                    print '# Number:', index
                    print result, '-' * 70
                    # result.download(settings['download path'] + key_word + ' ' + str(index) + '/')
                    if (index % 10) == 0:
                        if raw_input() == 'exit':
                            break
                else:
                    print 'No more results!'
            except ExtractError:
                print RED + 'Can\'t parse the web page' + RESET
                continue
        else:
            print 'No Results!'
