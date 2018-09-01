import sys

# import Settings
from .SearchEngine import ExtractError
from .SearchEngine.ThePirateBay import ThePirateBay
from .SearchEngine.EZTV import EZTV
from .SearchEngine.ZiMuKu import ZiMuKu
from .SearchEngine.IMDb import IMDb


def run():
    # settings = Settings.load()
    ses = [ThePirateBay(), EZTV(), ZiMuKu(), IMDb()]
    while True:
        print('# input 1: ThePirateBay')
        print('# input 2: EZTV')
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
        results_num = se.search(key_word)
        if results_num > 0:
            print('# Found', results_num, 'results')
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
            except ExtractError as e:
                sys.stderr.write(str(e))
                continue
        else:
            print('No Results!')
