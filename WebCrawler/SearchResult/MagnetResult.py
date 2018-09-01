# import transmission_rpc

from . import SearchResult

# tc = transmission_rpc.Client('localhost', 9091, 'admin', 'admin')


class MagnetResult(SearchResult):
    pass

    # def download(self, path):
    #     if self.torrent is None:
    #         self.__dict__['torrent'] = tc.add_torrent(self.link, download_dir=path)
