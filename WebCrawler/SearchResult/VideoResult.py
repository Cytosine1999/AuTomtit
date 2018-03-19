from __init__ import SearchResult
from Matcher.DictionaryMatcher import DictionaryMatcher
from Matcher.SizeMatcher import get_size


class VideoResult(SearchResult):
    @classmethod
    def set(cls):
        cls.MATCHER = {}
        for key, value in cls.VIDEO_RESULT_SETTINGS.iteritems():
            upper_key = key.upper()
            cls.MATCHER[upper_key] = DictionaryMatcher(value)

    def rate(self):
        s = self.RESOLUTION.match(self.name)
        s += self.UPLOADER.match(self.uploader)
        return s + get_size(self.size)
