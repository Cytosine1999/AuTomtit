# import Settings
from WebCrawler.SearchEngine import ExtractError
from WebCrawler.SearchEngine.ThePirateBay import ThePirateBay
from WebCrawler.SearchEngine.EZTV import EZTV
from WebCrawler.SearchEngine.ZiMuKu import ZiMuKu
from WebCrawler.SearchEngine.IMDb import IMDb

RED = '\033[31m'
BLUE = '\033[4;;34m'
RESET = '\033[0m'


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
        if se.search(key_word):
            print('# Showing results 10 at a time')
            print('# press enter to show next 10 results')
            print('# or input \"exit\" to exit')
            print('-' * 70)
            try:
                for i, result in enumerate(se.results()):
                    index = i + 1
                    print('# Number:', index)
                    print(result)
                    print('-' * 70)
                    # result.download(settings['download path'] + key_word + ' ' + str(index) + '/')
                    if (index % 10) == 0:
                        if input() == 'exit':
                            break
                else:
                    print('No more results!')
            except ExtractError:
                print(RED + 'Can\'t parse the web page' + RESET)
                continue
        else:
            print('No Results!')
