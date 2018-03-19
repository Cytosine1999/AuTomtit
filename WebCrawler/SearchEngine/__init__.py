from Tools.WebPageGrabber import WebPageGrabber


# version 1.0


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
    # you may need to modify some of the values
    def __init__(self):
        # this member is for 'WebPageGrabber'
        self.num_retries = 2
        # this member is decode language for 'BeautifulSoup'
        self.language = 'html5lib'
        # this member is used for grabbing page
        self.grabber = WebPageGrabber(self.__class__.__name__, True)
        # this member stores the current key word
        self.key_word = ''
        # this member stores current page index
        self.cur_num_page = 0
        # this member stores 'BeautifulSoup' object of current page
        self.cur_page = None

    # reset
    def reset(self):
        self.key_word = ''
        self.cur_num_page = 0
        self.cur_page = None

    # you need to override this function to return the correct url
    def generate_url(self, page=0):
        raise NotImplementedError

    def html_parse(self, url):
        respond = self.grabber.parse_page(url, self.__class__.__name__, self.language, self.num_retries)
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
    def search(self, key_word):
        self.reset()
        self.key_word = key_word
        return self.mod_current_page()

    # first test
    # you may need to override it
    def first_test(self):
        return self.test()

    # test whether there is result
    # you need to override it
    def test(self):
        raise NotImplementedError

    # return an iterator of results
    def results(self):
        try:
            while True:
                for result in self.results_in_page():
                    yield result
                if not self.mod_current_page(self.cur_num_page + 1):
                    break
        except Exception as e:
            raise ExtractError(e)

    # return an iterator of results in one page
    # you need to override it
    def results_in_page(self):
        raise NotImplementedError
