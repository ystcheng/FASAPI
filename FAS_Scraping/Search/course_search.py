from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
import pprint
from Object.course_obj import CourseObj
import json

import requests
import os

class CourseSearch:
    _url: str

    def __init__(self):
        # path = os.path.dirname(os.path.abspath(__file__))
        # self._url = os.path.join(
        #     path, 'Testing\courseSearch.html'
        # )
        self._url = 'https://fas.calendar.utoronto.ca/search-courses?page=0'

    def course_search(self) -> List:
        result = []
        # soup = BeautifulSoup(open(self._url), 'html.parser')
        soup = BeautifulSoup(requests.get(self._url).text, 'html.parser')
        data = soup.find(attrs={'summary': 'FAS Course Search Results'})
        table_soup = BeautifulSoup(str(data), 'html.parser')
        course_soup = BeautifulSoup(str(table_soup.find('tbody')), 'html.parser')
        course_row = course_soup.find_all('tr')

        for row in course_row:
            result.append(self._clean_course(row.getText()).get_info())

        return result

    def _clean_course(self, course_text: str) -> CourseObj:
        raw_course_info_list = course_text.strip().split('\n\n')
        raw_course_info_list.extend(
            ['']*(abs(5 - len(raw_course_info_list)))
        )

        code = raw_course_info_list[0].strip()
        title = raw_course_info_list[1].strip()
        description = raw_course_info_list[2].strip()
        prerequisite = raw_course_info_list[3].strip()
        exclusion = raw_course_info_list[4].strip()

        return CourseObj(code, title, description, prerequisite, exclusion)


if __name__ == '__main__':
    test = CourseSearch()
    print(json.dumps(test.course_search(), indent=2))
