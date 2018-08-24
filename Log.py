import threading

COLOR = {
    'red': '\033[31m',
    'blue': '\033[34m',
    'blue_u': '\033[4;;34m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'default': '\033[0m'
}


class Log:
    LOCK = threading.Lock()

    def __init__(self, source=None, color='default'):
        self.source = source
        self.color = COLOR[color]

    def msg(self, info, message, **kwargs):
        string = ''
        if self.source is not None:
            string += self.color + '[' + self.source
            if info is not None:
                string += ':' + info
            string += ']'
            if 'linebreak' in kwargs and kwargs['linebreak']:
                string += '\n'
            else:
                string += ' '
        for each in message:
            string += COLOR[each[1]] + each[0]
        string += COLOR['default']
        if 'print' in kwargs and kwargs['print']:
            self.LOCK.acquire()
            print(string)
            self.LOCK.release()
        elif 'file' in kwargs:
            pass
        return string
