import os

from .__init__ import SearchResult
from WebCrawler.Tools.Matcher import DictionaryMatcher
from WebCrawler.Tools.Decompresser import decompress
from WebCrawler.Tools.WebPageGrabber import WebPageGrabber


class SubtitleResult(SearchResult):
    wpg = WebPageGrabber.get()

    @classmethod
    def set(cls):
        cls.MATCHER.update({
            'author': DictionaryMatcher(cls.SUBTITLE_RESULT_SETTINGS['author']),
            'language': DictionaryMatcher(cls.SUBTITLE_RESULT_SETTINGS['language'])
        })

    def rate(self):
        s = SubtitleResult.MATCHER['author'].match(self.author)
        return s + SubtitleResult.MATCHER['language'].match(self.language)

    def download(self, file_path=''):
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_name = (file_path + self.name).encode('utf-8')
        self.wpg.download(self.link, file_name)
        decompress(file_name)
