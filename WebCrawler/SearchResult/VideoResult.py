from __init__ import SearchResult
from Tools.DictionaryMatcher import DictionaryMatcher, ValueMatcher
from Tools.StrToVal import get_size


class VideoResult(SearchResult):
    @classmethod
    def set(cls):
        cls.MATCHER.update({
            'resolution': DictionaryMatcher(cls.VIDEO_RESULT_SETTINGS['resolution']),
            'uploader': DictionaryMatcher(cls.VIDEO_RESULT_SETTINGS['uploader']),
            'size': ValueMatcher(cls.VIDEO_RESULT_SETTINGS['size'])
        })

    def rate(self):
        resolution = VideoResult.MATCHER['resolution'].match(self.name)
        uploader = VideoResult.MATCHER['uploader'].match(self.uploader)
        file_size = get_size(self.size)
        size = VideoResult.MATCHER['size'].match(file_size)
        # return s + get_size(self.size)
        # print 'resolution:', resolution
        # print 'uploader:', uploader
        return resolution + uploader + size


VideoResult.load()
