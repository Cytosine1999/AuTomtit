from __init__ import SearchResult
from Tools.Matcher import DictionaryMatcher, ValueMatcher
from Tools.StringResolve import get_size


class VideoResult(SearchResult):
    @classmethod
    def set(cls):
        cls.MATCHER.update({
            'resolution': DictionaryMatcher(cls.VIDEO_RESULT_SETTINGS['resolution']),
            'size': ValueMatcher(cls.VIDEO_RESULT_SETTINGS['size'])
        })

    def rate(self):
        resolution = VideoResult.MATCHER['resolution'].match(self.name)
        size = VideoResult.MATCHER['size'].match(get_size(self.size))
        return resolution + size


VideoResult.load()
