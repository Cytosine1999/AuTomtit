import re

from SearchResult import SearchResult

P_1080 = re.compile('1080')
P_720 = re.compile('720')


class VideoResult(SearchResult):
    def test(self):
        pass

    def rate(self):
        resolution = 0
        if self.name is not None:
            if P_1080.match(self.name):
                resolution += 80
            elif P_720.match(self.name):
                resolution += 70
