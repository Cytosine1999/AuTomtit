import os
import re

from . import SearchEngine
from ..SearchResult import SearchResult


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
        return IMDb.get_id(self.parent_id)

    def download_poster(self, path):
        link = self.poster_link
        if link is not None:
            if not os.path.exists(path):
                os.makedirs(path)
            self.wpg.download(link, path + '/' + self.name + '.jpg')


class IMDb(SearchEngine, new_slots=('details',)):
    DOMAIN_BASE = 'https://www.imdb.com'
    BRACKET = re.compile('\((.*?)\)', re.DOTALL)
    IMDB_ID = re.compile('(nm|tt)\d+')
    SEASON_EPISODE = re.compile('[Ss].*?(?P<season>\d+).*?[Ee].*?(?P<episode>\d+)', re.DOTALL)

    def __init__(self):
        SearchEngine.__init__(self)
        self.details = False

    def generate_url(self, page=0):
        head = 'https://www.imdb.com/find?ref_=nv_sr_fn&q='
        tail = '&s=tt'
        return head + self.url_parse(self.key_words) + tail

    def get_results_num(self):
        string = next(self._cur_page.select('h1.findHeader')[0].stripped_strings).split()
        return 0 if string[0] == 'No' else int(string[1])

    def test(self):
        return False

    def results_in_page(self):
        for each in self.extract_search_page(self._cur_page):
            item = IMDbResult(**self.extract_search_item(each))
            if self.details:
                item.update(**self.get_id(item.id, informed=True))
            yield item

    @classmethod
    def extract_search_page(cls, page):
        return page.select('table.findList')[0].select('tr')

    @classmethod
    def extract_search_item(cls, item):
        info = item.select('td.result_text')[0]
        info_strings = info.stripped_strings
        name = next(info_strings)
        IMDb_id = cls.IMDB_ID.search(info.a['href']).group()
        description = cls.BRACKET.findall(next(info_strings))
        reference = info.select('small')
        se_ep = cls.unwrap(lambda: cls.SEASON_EPISODE.search(cls.un_strings(reference[0])))
        reference_string = cls.unwrap(lambda: reference[1].stripped_strings)
        cls.unwrap(lambda: next(reference_string))
        parent_name = cls.unwrap(lambda: next(next(reference_string)))
        parent_description = cls.unwrap(lambda: cls.BRACKET.search(next(reference_string)))
        return {
            'name': name,
            'id': IMDb_id,
            # What if msg have type but no time?
            'time': cls.unwrap(lambda: description[0] if len(description[0]) == 4 else None),
            'type': cls.unwrap(lambda: description[1]),
            'aka': cls.unwrap(lambda: info.select('i')[0].string),
            'season': cls.unwrap(lambda: int(se_ep.group('season'))),
            'episode': cls.unwrap(lambda: int(se_ep.group('episode'))),
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
                url = 'https://www.imdb.com/title/' + IMDb_id + '/episodes?season=' + str(kwargs['season'])
                season_list = cls.extract_season_page(cls.html_parse(url))
                if 'episode' in kwargs:
                    return cls.unwrap(lambda: cls.extract_season_item(season_list[kwargs['episode']]))
                else:
                    @cls.unwrap
                    def season_iter():
                        for item in season_list:
                            episode_item = cls.extract_season_item(item)
                            if episode_item['season'] == kwargs['season']:
                                yield episode_item
                            else:
                                break

                    return season_iter
            else:
                url = 'https://www.imdb.com/title/' + IMDb_id + '/'
                if 'informed' in kwargs:
                    informed = kwargs['informed']
                else:
                    informed = False
                return cls.extract_title_page(cls.html_parse(url), informed)
        elif head == 'nm':
            return 'https://www.imdb.com/name/' + IMDb_id + '/'

    @classmethod
    def extract_season_page(cls, page):
        return page.select('div.list_item')

    @classmethod
    def extract_season_item(cls, item):
        image = item.select('div.image')[0].a
        se_ep = cls.SEASON_EPISODE.findall(next(image.stripped_strings))[0]
        info = item.select('div.info')[0]
        return {
            'name': info.strong.string,
            'id': cls.IMDB_ID.search(image['href']).group(),
            'season': int(se_ep.group('season')),
            'episode': int(se_ep.group('episode')),
            'time': info.select('div.airdate')[0].string.strip(),
            'rate': info.select('span.ipl-rating-star__rating')[0].string,
            'summary': info.select('div.item_description')[0].string.strip()
        }

    @classmethod
    def extract_title_page(cls, page, informed=False):
        over_view = page.find(id='title-overview-widget')
        title_bar = over_view.select('div.title_bar,.titleBar')[0]
        ratings_wrapper = cls.unwrap(lambda: over_view.select('div.ratings_wrapper')[0])
        sub_text = cls.unwrap(lambda: title_bar.select('div.subtext')[0])
        plot_summary = cls.unwrap(lambda: over_view.select('div.plot_summary_wrapper')[0])
        episode_list = cls.unwrap(lambda: page.find(id='title-episode-widget').select('div.seasons-and-year-nav')[0])
        results = {}

        @cls.unwrap
        def credit_summaries():
            for each in cls.unwrap(lambda: plot_summary.select('div.credit_summary_item')):
                staffs = each.select('> span')
                value = {}
                for staff in staffs:
                    try:
                        value[staff.select('span')[0].string] = cls.IMDB_ID.search(staff.a['href']).group()
                    except TypeError:
                        pass
                results[each.h4.string.replace(':', '')] = value
            return results

        item = {
            'rate': cls.unwrap(lambda: ratings_wrapper.select('strong > span')[0].string),
            'duration': cls.unwrap(lambda: sub_text.time.string.strip()),
            'category': cls.unwrap(lambda: cls.un_list(sub_text.select('span.itemprop'))),
            'poster_link': cls.unwrap(lambda: over_view.select('div.poster img')[0]['src']),
            'summery': cls.unwrap(lambda: plot_summary.select('div.summary_text')[0].string.strip()),
            'credit_summaries': credit_summaries,
            'season_num': cls.unwrap(lambda: int(episode_list.a.string))
        }
        if not informed:  # TODO
            title_parent = cls.unwrap(lambda: over_view.select('div.titleParent')[0])
            item.update({
                'name': cls.un_strings(title_bar.select('h1')[0]),
                'id': None,
                'time': None,
                'type': None,
                'aka': None,
                'season': None,
                'episode': None,
                'parent_name': cls.unwrap(lambda: title_parent.a.string),
                'parent_id': None,
                'parent_time': cls.unwrap(lambda: title_parent.span.string),
                'parent_type': None
            })
        return item

    @classmethod
    def extract_name_page(cls, page):
        pass  # TODO

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


if __name__ == '__main__':
    se = IMDb()
    se.search('better call saul')
    se.details = True
    for result in se.results():
        print(result)
