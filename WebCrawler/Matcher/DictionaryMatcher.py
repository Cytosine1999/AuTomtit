import re


class DictionaryMatcher:
    def __init__(self, dictionary, default):
        self.dictionary = []
        self.default = default
        for key, value in dictionary.iteritems():
            self.dictionary.append((re.compile(key, re.IGNORECASE), value))

    def add(self):
        pass    # TODO

    def match(self, string):
        for each in self.dictionary:
            if each[1].match(string):
                return each[2]
        return self.default

    def persist(self):
        pass   # TODO maybe

    def restore(self):
        pass    # TODO maybe
