import re

from ... import Settings


class SearchResult:
    @classmethod
    def load(cls):
        name = cls.__name__
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
        name += '_settings'
        cls.settings_name = name.replace('_', ' ')
        cls.member_name = name.upper()
        setattr(cls, cls.member_name, Settings.load()[cls.settings_name])
        if 'MATCHER' not in cls.__dict__:
            cls.MATCHER = {}
        cls.set()

    @classmethod
    def set(cls):
        pass

    @classmethod
    def dump(cls):
        profile = Settings.load()
        profile[cls.profile_name] = cls.__dict__[cls.member_name]
        Settings.dump(profile)

    __slots__ = ('name',)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                self.__setattr__(key, value)

    def __str__(self):
        string = self.__class__.__name__ + ':\n'
        for key, value in self.__dict__.items():
            string += str(key) + ': ' + str(value) + '\n'
        return string

    def __getattr__(self, item):
        return None

    def update(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def rate(self):
        return 0
