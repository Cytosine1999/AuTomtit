from SearchResult import SearchResult
from Matcher.DictionaryMatcher import DictionaryMatcher

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


class VideoResult(SearchResult):
    def rate(self):
        resolution = 0
        if self.name is not None:
            resolution = RESOLUTION.match(self.name)
        return resolution
