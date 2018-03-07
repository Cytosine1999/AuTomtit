from SearchResult import SearchResult
from Matcher.DictionaryMatcher import DictionaryMatcher
from Matcher.SizeMatcher import get_size


class VideoResult(SearchResult):
    RESOLUTION = DictionaryMatcher({
        '4K': 95,
        '1080P': 90,
        '1080I': 85,
        '1080': 82,
        '720P': 80,
        '720I': 75,
        '720': 72,
        'default': 50
    })
    UPLOADER = DictionaryMatcher({
        'default': 50
    })

    def rate(self):
        s = self.RESOLUTION.match(self.name)
        s += self.UPLOADER.match(self.uploader)
        s += get_size(self.size)
        return s
