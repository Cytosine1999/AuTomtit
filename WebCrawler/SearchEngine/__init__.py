from WebCrawler.Tools.WebPageGrabber import WebPageGrabber


class SearchError(Exception):
    pass


class WebError(SearchError):
    pass


class ExtractError(SearchError):
    def __init__(self, e):
        self.e = e

    def __str__(self):
        return str(self.e)


# a super class of search engines
# you may need to modify the time limit between each grabbing action which has a default value one minute
class SearchEngine:
    @classmethod
    def set(cls, time_limit={}, time_out=60, retries=2):
        # this member is used for grabbing page
        cls.grabber = WebPageGrabber.get()
        cls.grabber.timeout = time_out
        cls.language = 'html5lib'
        cls.num_retries = retries
        for key, value in time_limit.items():
            cls.grabber.mod_site(key, value)

    # you may need to modify some of the values
    def __init__(self):
        # this member stores the current key word
        self.key_words = ''
        # this member stores current page index
        self.cur_num_page = 0
        # this member stores 'BeautifulSoup' object of current page
        self.cur_page = None

    # reset
    def reset(self):
        self.key_words = ''
        self.cur_num_page = 0
        self.cur_page = None

    # you need to override this function to return the correct url
    def generate_url(self, page=0):
        raise NotImplementedError

    @classmethod
    def html_parse(cls, url):
        respond = cls.grabber.parse_page(url, cls.language, cls.num_retries)
        if respond is None:
            raise WebError()
        else:
            return respond

    # this function carries out grabbing action
    def mod_current_page(self, page=0):
        self.cur_page = self.html_parse(self.generate_url(page))
        if self.cur_page is None:
            return False
        if page == 0:
            if not self.first_test():
                return False
        else:
            if not self.test():
                return False
        self.cur_num_page = page
        return True

    # set a new key word
    def search(self, key_words):
        self.reset()
        self.key_words = key_words
        return self.mod_current_page()

    # first test
    # you may need to override it
    def first_test(self):
        return self.test()

    # test whether there is result
    # you need to override it
    def test(self):
        raise NotImplementedError

    def result(self):
        return next(self.results())

    # return an iterator of results
    def results(self):
        # try:
        while True:
            for result in self.results_in_page():
                yield result
            if not self.mod_current_page(self.cur_num_page + 1):
                break
        # except Exception as e:
        #     raise ExtractError(e)

    # return an iterator of results in one page
    # you need to override it
    def results_in_page(self):
        raise NotImplementedError

    @staticmethod
    def unwrap(fn):
        try:
            return fn()
        except (IndexError, AttributeError, TypeError):
            return None
