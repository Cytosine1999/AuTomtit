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

    def add(self):
        pass    # TODO

    def match(self, string):
        if string is None:
            return self.default
        for each in self.dictionary:
            if each[1].match(string):
                return each[2]
        return self.default

    def persist(self):
        pass   # TODO maybe

    def restore(self):
        pass    # TODO maybe
