import transmissionrpc

from SearchResult import SearchResult

tc = transmissionrpc.Client('localhost', 9091, 'transmission', 'ubuntu')


class MagnetResult(SearchResult):
    def download(self):
        if self.torrent is None:
            self.__dict__['torrent'] = tc.add_torrent(self.link) # TODO return type
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

    """
    tc = transmissionrpc.Client('localhost', 9091, 'transmission', 'ubuntu')
    se = HaiDaoWan()
    se.search('this is us')
    result = se.results().next()
    download = tc.add_torrent(result.link)
    print 'downloading:'
    print result
    has = download.hashString
    print has
    print tc.get_torrents()
    time.sleep(10)
    tc.stop_torrent(has)
    tc.remove_torrent(has)
    print tc.get_torrents()
    """