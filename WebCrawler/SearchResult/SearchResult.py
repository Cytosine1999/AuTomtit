class SearchResult:
    def __init__(self, result):
        self.__dict__.update(result)

    def __str__(self):
        string = self.__class__.__name__ + ':\n'
        for each in self.__dict__:
            string += str(each) + ': ' + str(self.__dict__[each]) + '\n'
        return string
