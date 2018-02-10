class SearchResult:
    def __init__(self, **result):
        self.rate = 0
        self.__dict__.update(result)

    def __str__(self):
        string = self.__class__.__name__ + ':\n'
        for each in self.__dict__:
            string += str(each) + ': ' + str(self.__dict__[each]) + '\n'
        return string

    def __getattr__(self, item):
        try:
            return self.__dict__[item]
        except KeyError:
            return None

    def test(self):
        pass

    def rate(self):
        return 0
