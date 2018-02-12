import re


class DictionaryMatcher:
    def __init__(self, dictionary, default):
        self.dictionary = []
        self.default = default
        for key, value in dictionary.iteritems():
            self.dictionary.append((re.compile(key), value))

    def add(self):
        pass    # TODO

    def match(self, string):
        for pattern, value in self.dictionary:
            if pattern.match(string):
                return value
        return self.default

    def persist(self):
        pass   # TODO maybe

    def restore(self):
        pass    # TODO maybe
