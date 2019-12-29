from bs4 import BeautifulSoup
from typing import *
import requests


class ScrapingFAS:
    _url: str
    _course_code: str
    _course_title: str
    _description: str
    _prerequisite: str
    _exclusion: str
    _scraped_result: List[Dict]

    def __init__(self) -> None:
        self._url = 'https://fas.calendar.utoronto.ca/search-courses?page=0'
        self._course_code = 'views-field-title'
        self._course_title = 'views-field-field-course-title'
        self._description = 'views-field-body'
        self._prerequisite = 'views-field-field-prerequisite1'
        self._exclusion = 'views-field-field-exclusion1'
        self._scraped_result = []

    def scraping(self) -> List[Dict]:
        raw_html = requests.get(self._url)
        soup = BeautifulSoup(raw_html.text, 'html.parser')

        data = soup.find_all('tr')[2:]

        final_data = []

        for item in data:
            final_data.append(self._inner_scraping(item.contents))

        self._scraped_result = list(filter(None, final_data))

        return self._scraped_result

    def _inner_scraping(self, inner_data: List) -> Dict:

        def return_target(inner_item: List) -> str:
            for item in inner_item:
                if item.name == 'a':
                    return item.text
            return ''

        def reconstruct(stuff: dict, key: str, value: str, replace: str) -> None:
            if value == '':
                stuff[key] = replace.strip()
            else:
                stuff[key] = value.strip()

        result = {}
        for item in inner_data:
            try:
                if self._course_code in item.attrs['class']:

                    reconstruct(result, 'Course Code',
                                return_target(item.contents), item.text)

                elif self._course_title in item.attrs['class']:
                    reconstruct(result, 'Course Title',
                                return_target(item.contents), item.text)
                elif self._description in item.attrs['class']:
                    reconstruct(result, 'Description',
                                return_target(item.contents), item.text)
                elif self._prerequisite in item.attrs['class']:
                    reconstruct(result, 'Prerequisite',
                                return_target(item.contents), item.text)
                elif self._exclusion in item.attrs['class']:
                    reconstruct(result, 'Exclusion',
                                return_target(item.contents), item.text)
            except:
                pass

        return result

    def get_recent_scraped(self) -> List[Dict]:
        return self._scraped_result

    def __str__(self):
        if len(self._scraped_result) == 0:
            print('')

        result = ''

        for item in self._scraped_result:
            inner_str = ''
            for key in item:
                inner_str += key + ': ' + item[key] + '\n'

            result += inner_str + '\n'

        print(result.strip())


if __name__ == '__main__':
    test = ScrapingFAS()
    test.scraping()
    print(test.__str__())
