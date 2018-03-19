import os

from __init__ import SearchResult
from Matcher.DictionaryMatcher import DictionaryMatcher
from Tools.Decompresser import decompress


class SubtitleResult(SearchResult):
    @classmethod
    def set(cls):
        cls.MATCHER = {}
        for key, value in cls.SUBTITLE_RESULT_SETTINGS.iteritems():
            upper_key = key.upper()
            cls.MATCHER[upper_key] = DictionaryMatcher(value)

    def rate(self):
        s = self.AUTHOR.match(self.author)
        return s + self.LANGUAGE.match(self.language)

    def download(self, file_path=''):
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_name = (file_path + self.name).encode('utf-8')
        self.wpg.download(self.link, file_name)
        decompress(file_name)
