from bs4 import BeautifulSoup
from typing import *
from Object.course_obj import CourseObj
from pprint import pprint
from multiprocessing import Pool, Queue, Process
import math

import requests


class CourseScraping:

    def __init__(self):
        self._url = 'https://fas.calendar.utoronto.ca/search-courses?page=0'
        self._urls = self._generate_urls()

    # def scraping(self) -> List[CourseObj]:
    #     raw_html = requests.get(self._url)
    #     soup = BeautifulSoup(raw_html.text, 'html.parser')
    #
    #     data = soup.find('table', attrs={'summary': 'FAS Course Search Results'})
    #
    #     response = self._remove_empty_element(
    #         self._remove_empty_element(data.contents)[1].contents
    #     )
    #
    #     code = 0
    #     title = 1
    #     description = 2
    #     prerequisite = 3
    #     exclusion = 4
    #
    #     result = []
    #
    #     for res in response:
    #         info = list(filter(None, res.text.split('\n')))
    #         result.append(
    #             [self._get_info(code, info),
    #             self._get_info(title, info),
    #             self._get_info(description, info),
    #             self._get_info(prerequisite, info),
    #             self._get_info(exclusion, info)]
    #         )
    #
    #     return result

    def t_scraping(self, url, out_queue):
        result = []
        for i in url:
            raw_html = requests.get(i)
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

            for res in response:
                info = list(filter(None, res.text.split('\n')))
                result.append(
                    [self._get_info(code, info),
                    self._get_info(title, info),
                    self._get_info(description, info),
                    self._get_info(prerequisite, info),
                    self._get_info(exclusion, info)]
                )

        out_queue.put(result)


    def scrape_all(self) -> List[CourseObj]:
        out_queue = Queue()
        num_procs = 4
        chunksize = int(math.ceil(len(self._urls)) / float(num_procs))
        procs = []

        for i in range(num_procs):
            p = Process(
                target=self.t_scraping,
                args=(self._urls[chunksize * i:chunksize * (i+1)], out_queue)
            )
            procs.append(p)
            p.start()

        result = []
        for i in range(2):
            result.extend(out_queue.get())
        for p in procs:
            p.join()
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

    def _generate_urls(self) -> List:
        # iteration = self._get_max_url_num()
        iteration = self._get_max_url_num()
        result = []
        base = 'https://fas.calendar.utoronto.ca/search-courses?page='
        for i in range(iteration):
            result.append(base + str(i))
        return result

    def _get_max_url_num(self) -> int:
        raw_html = requests.get(self._url)
        soup = BeautifulSoup(raw_html.text, 'html.parser')
        data = soup.find('li', attrs={'class': 'pager-current'}).get_text()
        print(int(data.split()[-1]))
        return data.split()[-1]


if __name__ == '__main__':
    test = CourseScraping()
    pprint(test.scrape_all())
    # pprint(test.scraping())
