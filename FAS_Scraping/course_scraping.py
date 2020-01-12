from bs4 import BeautifulSoup
from typing import *
from Object.course_obj import CourseObj
from pprint import pprint

import requests


class CourseScraping:

    def __init__(self):
        self._url = 'https://fas.calendar.utoronto.ca/search-courses?page=0'

    def scraping(self) -> List[CourseObj]:
        raw_html = requests.get(self._url)
        soup = BeautifulSoup(raw_html.text, 'html.parser')

        data = soup.find('table', attrs={'summary': 'FAS Course Search Results'})

        response = self._remove_empty_element(
            self._remove_empty_element(data.contents)[1].contents
        )

        code = 0
        title = 1
        description = 2
        prerequisite = 3
        exclusion = 4

        result = []

        for res in response:
            info = list(filter(None, res.text.split('\n')))
            result.append(
                [self._get_info(code, info),
                self._get_info(title, info),
                self._get_info(description, info),
                self._get_info(prerequisite, info),
                self._get_info(exclusion, info)]
            )

        return result

    def _get_info(self, index: int, info_list: List) -> str:
        try:
            return info_list[index].strip()
        except IndexError:
            return ''



    def _filter_useless_space(self, input_str: str) -> bool:
        try:
            input_str.strip()
            return False
        except TypeError:
            return True

    def _remove_empty_element(self, input_list) -> List:
        return list(filter(self._filter_useless_space, input_list))

if __name__ == '__main__':
    test = CourseScraping()
    pprint(test.scraping())
