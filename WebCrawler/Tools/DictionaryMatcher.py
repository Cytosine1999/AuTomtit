import re


class DictionaryMatcher:
    def __init__(self, dictionary):
        self.dictionary = []
        self.default = None
        for key, value in dictionary.iteritems():
            if key == 'default':
                self.default = value
            else:
                self.dictionary.append((re.compile(key, re.IGNORECASE), value))

    def match(self, string):
        if string is None:
            return self.default
        for each in self.dictionary:
            if each[0].match(string):
                return each[1]
        return self.default

    def reflect(self):
        pass


class ValueMatcher:
    def __init__(self, arg):
        self.ratio = arg['ratio']
        self.maximum = arg['maximum']

    def match(self, value):
        return min(self.ratio * value, self.maximum)

    def reflect(self):
        pass
