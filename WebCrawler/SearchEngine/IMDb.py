import urllib2
import re

from __init__ import SearchEngine
from WebCrawler.SearchResult import SearchResult


class IMDbResult(SearchResult):
    def get_type(self):
        pass

    def get_episode(self, season, episode):
        return IMDb.get_id(self.id, season=season, episode=episode)

    def get_episodes(self):
        for season in range(1, self.season_num + 1):
            for episode in self.get_season(season):
                yield episode

    def get_season(self, season):
        return IMDb.get_id(self.id, season=season)

    def get_parent(self):
        pass


class IMDb(SearchEngine):
    DOMAIN = 'http://www.imdb.com'
    PAREN = re.compile('\((.*?)\)', re.DOTALL)
    IMBD_ID = re.compile('nm\d+|tt\d+')
    SE_EP = re.compile('[Ss]\w*?(\d+),\s*[Ee]\w*?(\d+)')

    def __init__(self):
        SearchEngine.__init__(self)
        self.details = False

    def generate_url(self, page=0):
        head = 'http://www.imdb.com/find?ref_=nv_sr_fn&q='
        tail = '&s=tt'
        return head + urllib2.quote(self.key_word) + tail

    def first_test(self):
        return True

    def test(self):
        return False

    def results_in_page(self):
        for item in self.extract_search_page(self.cur_page):
            result = self.extract_search_item(item)
            if self.details:
                result.update(self.get_id(result['id']))
            yield IMDbResult(result)

    @classmethod
    def extract_search_page(cls, page):
        return page.select('table.findList')[0].select('tr')

    @classmethod
    def extract_search_item(cls, item):
        info = item.select('td.result_text')[0]
        info_strings = info.stripped_strings
        name = info_strings.next()
        IMDb_id = cls.IMBD_ID.findall(info.a['href'])[0]
        description = cls.PAREN.findall(info_strings.next())
        reference = info.select('small')
        episode_info = cls.unwrap(lambda: cls.un_strings(reference[0]).split())
        reference_string = cls.unwrap(lambda: reference[1].stripped_strings)
        cls.unwrap(lambda: reference_string.next())
        parent_name = cls.unwrap(lambda: reference_string.next())
        parent_description = cls.unwrap(lambda: cls.PAREN.findall(reference_string.next()))
        return {
            'name': name,
            'id': IMDb_id,
            # What if msg have type but no time?
            'time': cls.unwrap(lambda: description[0] if len(description[0]) == 4 else None),
            'type': cls.unwrap(lambda: description[1]),
            'aka': cls.unwrap(lambda: info.select('i')[0].string),
            'season': cls.unwrap(lambda: int(episode_info[2])),
            'episode': cls.unwrap(lambda a: int(episode_info[5])),
            'parent_name': parent_name,
            'parent_id': cls.unwrap(lambda: reference[1].a['href'].split('/')[2]),
            'parent_time': cls.unwrap(lambda: parent_description[0] if len(parent_description[0]) == 4 else None),
            'parent_type': cls.unwrap(lambda: parent_description[1])
        }

    @classmethod
    def get_id(cls, IMDb_id, **kwargs):
        head = IMDb_id[:2]
        if head == 'tt':
            if 'season' in kwargs:
                url = 'http://www.imdb.com/title/' + IMDb_id + '/episodes?season=' + str(kwargs['season'])
                season_list = cls.extract_season_page(cls.html_parse(url))
                if 'episode' in kwargs:
                    return cls.extract_season_item(season_list[kwargs['episode']])
                else:
                    def season_iter():
                        for item in season_list:
                            yield cls.extract_season_item(item)
                    return season_iter()
            else:
                url = 'http://www.imdb.com/title/' + IMDb_id + '/'
                return cls.extract_title_page(cls.html_parse(url))
        elif head == 'nm':
            return 'http://www.imdb.com/name/' + IMDb_id + '/'

    @classmethod
    def extract_season_page(cls, page):
        return page.select('div.list_item')

    @classmethod
    def extract_season_item(cls, item):
        image = item.select('div.image')[0].a
        se_ep = cls.SE_EP.findall(image.stripped_strings.next())[0]
        info = item.select('div.info')[0]
        return {
            'id': cls.IMBD_ID.findall(image['href'])[0],
            'season': int(se_ep[0]),
            'episode': int(se_ep[1]),
            'time': info.select('div.airdate')[0].string.strip(),
            'rate': info.select('span.ipl-rating-star__rating')[0].string,
            'summary': info.select('div.item_description')[0].string.strip()
        }

    @classmethod
    def extract_title_page(cls, page):
        over_view = page.find(id='title-overview-widget')
        title_bar = over_view.select('div.title_bar,.titleBar')[0]
        ratings_wrapper = cls.unwrap(lambda: over_view.select('div.ratings_wrapper')[0])
        sub_text = cls.unwrap(lambda: title_bar.select('div.subtext')[0])
        plot_summary = cls.unwrap(lambda: over_view.select('div.plot_summary_wrapper')[0])
        episode_list = cls.unwrap(lambda: page.find(id='title-episode-widget'))

        @IMDb.unwrap
        def credit_summaries():
            results = {}
            for item in cls.unwrap(lambda: plot_summary.select('div.credit_summary_item')):
                credits = item.select('> span')
                value = {}
                for credit in credits:
                    try:
                        value[credit.select('span')[0].string] = cls.IMBD_ID.findall(credit.a['href'])[0]
                    except Exception:
                        pass
                results[item.h4.string.replace(':', '')] = value
            return results

        return {
            'rate': cls.unwrap(lambda: ratings_wrapper.select('strong > span')[0].string),
            'duration': cls.unwrap(lambda: sub_text.time.string.strip()),
            'category': cls.unwrap(lambda: cls.un_list(sub_text.select('span.itemprop'))),
            'poster_link': cls.unwrap(lambda: over_view.select('div.poster img')[0]['src']),
            'summery': cls.unwrap(lambda: plot_summary.select('div.summary_text')[0].string.strip()),
            'credit_summaries': credit_summaries,
            'season_num': cls.unwrap(lambda: int(episode_list.a.string))
        }

    @classmethod
    def extract_name_page(cls, page):
        pass

    @staticmethod
    def un_strings(strings):
        string = ''
        for each in strings.stripped_strings:
            string += each + ' '
        return string

    @staticmethod
    def un_list(obj):
        string = ''
        for each in obj:
            string += each.string + ' '
        return string


IMDb.set(5, 10)
