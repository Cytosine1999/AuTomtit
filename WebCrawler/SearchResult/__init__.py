import copy


class ConstructionException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'ConstructionException: ' + self.msg


class SearchResultItem:
    @classmethod
    def pick_instances(cls, dictionary):
        pick = set(key for key, value in dictionary.items() if isinstance(value, cls))
        for each in pick:
            dictionary.pop(each)
        return pick

    def __set__(self, instance, value):
        pass

    def __get__(self, instance, owner):
        pass


# TODO bases
class SearchResultMeta(type):
    def __new__(mcs, name, bases, attrs, extends=()):
        if not name == 'SearchResult':
            if not (len(bases) == 1 and bases[0] == SearchResult):
                raise ConstructionException('You cannot extends class SearchResult while extending other classes.')
        slots = SearchResultItem.pick_instances(attrs)
        if not name == 'SearchResult':
            for each in extends:
                slots |= each.__slots__
        attrs['__slots__'] = slots
        return super(SearchResultMeta, mcs).__new__(mcs, name, bases, attrs)


class InitialException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'ConstructionException: ' + self.msg


class SearchResult(metaclass=SearchResultMeta):
    # def __init_subclass__(cls, **kwargs):
    #     print(cls.__slots__)

    def __init__(self, **kwargs):
        for filed in self.__slots__:
            try:
                self.__setattr__(filed, kwargs[filed])
            except KeyError:
                self.__setattr__(filed, None)

    def to_dict(self):
        return {key: value for key, value in self.items()}

    def update(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def items(self):
        for filed in self.__slots__:
            yield filed, self.__getattribute__(filed)

    def clone(self):
        return copy.deepcopy(self)

    def __repr__(self):
        return str(self.to_dict())
