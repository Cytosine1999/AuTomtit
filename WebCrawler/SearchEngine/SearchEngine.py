# coding:utf-8
from bs4 import BeautifulSoup
from WebPageGrabber import WebPageGrabber


# version 1.0

# a super class of search engines
# you may need to modify the time limit which has a default value one minute between each grabbing action
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
        self.num_results = 0
        self.num_page = 0

    # reset
    def reset(self):
        self.key_word = ''
        self.cur_num_page = 0
        self.cur_page = None
        self.num_results = 0
        self.num_page = 0

    # you need to override this function to return the correct url
    def generate_url(self, page=0):
        return ''

    # this function carries out grabbing action
    def mod_current_page(self, page=0):
        respond = self.grabber.grab_page(self.generate_url(page), self.__class__.__name__, self.num_retries)
        if respond is None:
            return False
        self.cur_page = BeautifulSoup(respond.read(), self.language)
        if not self.test():
            return False
        self.cur_num_page = page
        return True

    # set a new key word
    def search(self, key_word):
        self.reset()
        self.key_word = key_word
        if not self.mod_current_page():
            return self.num_results
        self.get_num()
        return self.num_results

    # test whether there is result
    # you need to override it
    def test(self):
        return False

    # get number of results and pages
    # you need to override it
    def get_num(self):
        pass

    # return an iterator of results
    # you need to override it
    def results(self):
        while False:
            yield None
