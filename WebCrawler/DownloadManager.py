from WebCrawler.SearchEngine.IMDb import IMDb

if __name__ == '__main__':
    se = IMDb()
    se.details = True
    se.search('doctor who')
    print se.results().next().get_episode(9, 12)
