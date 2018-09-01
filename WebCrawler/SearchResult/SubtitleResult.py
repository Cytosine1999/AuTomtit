import os

from . import SearchResult
from ..Tools.Decompresser import decompress
from ..Tools.WebPageGrabber import WebPageGrabber


class SubtitleResult(SearchResult):
    __WPG = WebPageGrabber()

    def download(self, file_path=''):
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_name = (file_path + self.name).encode('utf-8')
        WebPageGrabber.download(self.link, file_name)
        decompress(file_name)
