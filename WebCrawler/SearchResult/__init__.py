class SearchResult:
    def __init__(self, **result):
        self.__dict__.update(result)

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
