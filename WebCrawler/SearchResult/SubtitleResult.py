# coding:utf-8
from SearchResult import SearchResult
from Matcher.DictionaryMatcher import DictionaryMatcher


class SubtitleResult(SearchResult):
    AUTHOR = DictionaryMatcher({
        'YYeTs': 80,
        '字幕组': 50,
        'default': 20
    })

    LANGUAGE = DictionaryMatcher({
        '双语': 80,
        '简体中文': 50,
        'default': 20
    })

    def rate(self):
        s = self.AUTHOR.match(self.author)
        return s + self.LANGUAGE.match(self.language)

    def download(self):
        pass
