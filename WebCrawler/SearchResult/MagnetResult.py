import transmission_rpc

from .__init__ import SearchResult
from WebCrawler.Tools.Matcher import ValueMatcher

tc = transmission_rpc.Client('localhost', 9091, 'admin', 'admin')


class MagnetResult(SearchResult):
    @classmethod
    def set(cls):
        cls.MATCHER.update({
            'seeder': ValueMatcher(cls.MAGNET_RESULT_SETTINGS['seeder'])
        })

    def rate(self):
        seeder = MagnetResult.MATCHER['seeder'].match(self.num_seeder)
        return seeder

    def download(self, path):
        if self.torrent is None:
            self.__dict__['torrent'] = tc.add_torrent(self.link, download_dir=path)


MagnetResult.load()
