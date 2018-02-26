import transmissionrpc

from SearchResult import SearchResult

tc = transmissionrpc.Client('localhost', port=9091)


class MagnetResult(SearchResult):
    def download(self):
        pass
