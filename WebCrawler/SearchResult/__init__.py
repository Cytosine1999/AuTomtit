import re

import AuTomtit


class SearchResult:
    @classmethod
    def load(cls):
        name = cls.__name__
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
        name += '_settings'
        cls.profile_name = name.replace('_', ' ')
        cls.member_name = name.upper()
        cls.__dict__[cls.member_name] = AuTomtit.load()[cls.profile_name]
        cls.set()

    @classmethod
    def set(cls):
        cls.MATCHER = {}

    @classmethod
    def dump(cls):
        profile = AuTomtit.load()
        profile[cls.profile_name] = cls.__dict__[cls.member_name]
        AuTomtit.dump(profile)

    def __init__(self, **result):
        self.__dict__.update(result)
        if 'MATCHER' not in self.__class__.__dict__:
            self.load()

    def __str__(self):
        string = self.__class__.__name__ + ':\n'
        for key, value in self.__dict__.iteritems():
            string += str(key) + ': ' + str(value) + '\n'
        return string

    def __getattr__(self, item):
        try:
            return self.__dict__[item]
        except KeyError:
            return None

    def rate(self):
        return 0
