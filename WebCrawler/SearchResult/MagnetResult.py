import transmissionrpc

from .__init__ import SearchResult
from WebCrawler.Tools.Matcher import ValueMatcher

tc = transmissionrpc.Client('localhost', 9091, 'admin', 'admin')


class MagnetResult(SearchResult):
    @classmethod
    def set(cls):
        cls.MATCHER.update({
            'seeder': ValueMatcher(cls.MAGNET_RESULT_SETTINGS['seeder'])
        })

    def rate(self):
        seeder = MagnetResult.MATCHER['seeder'].match(self.num_seeder)
        return seeder

    def download(self):
        if self.torrent is None:
            self.__dict__['torrent'] = tc.add_torrent(self.link)  # TODO return type
        elif self.torrent.status == 'stopped':
            tc.start_torrent(self.torrent.id)

    def remove(self):
        # TODO can't remove data
        if self.torrent is None:
            return
        else:
            tc.remove_torrent(self.torrent.id)

    def stop(self):
        if self.torrent in None:
            return
        else:
            tc.stop_torrent(self.torrent.id)


MagnetResult.load()
