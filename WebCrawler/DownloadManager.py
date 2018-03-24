from WebCrawler.SearchEngine.IMDb import IMDb

if __name__ == '__main__':
    se = IMDb()
    se.search('doctor who')
    for result in se.results():
        print result
