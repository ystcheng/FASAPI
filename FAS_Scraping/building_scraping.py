from bs4 import BeautifulSoup
from typing import *
from Object.building_obj import BuildingObj
import requests


class ScrapingBuilding:

    def __init__(self):
        self._url = 'http://map.utoronto.ca/utsg/c/buildings'

    def scraping(self) -> List[BuildingObj]:
        parsed_data = []

        raw_html = requests.get(self._url)
        soup = BeautifulSoup(raw_html.text, 'html.parser')

        data = soup.find_all('ul', attrs={"class": ["buildinglist"]})

        test = self._remove_empty_element(data[0].contents)

        for item in test:
            result = self._loop_to_content(item)

            parsed_data.append(self._get_content_specific(result))

        return parsed_data

    def _loop_to_content(self, data: List) -> List:
        temp = self._remove_empty_element(data)

        if 0 < len(temp) < 3:
            return self._loop_to_content(temp[-1].contents)

        elif len(temp) == 3:
            return temp

        return []

    def _filter_useless_space(self, input_str: str) -> bool:
        try:
            input_str.strip()
            return False
        except TypeError:
            return True

    def _remove_empty_element(self, input_list) -> List:
        return list(filter(self._filter_useless_space, input_list))

    def _get_content_specific(self, content: List) -> BuildingObj:
        name = content[0].text
        address = content[1].text
        id = content[2].contents[0].attrs['href'].split('/')[-1].strip()
        return BuildingObj(
            id,
            name.split('|')[-1].strip(),
            name.split('|')[0].strip(),
            address.split(',')[0].strip(),
            address.split(',')[-1].strip()
        )


if __name__ == '__main__':
    test = ScrapingBuilding()
    result = test.scraping()

    for item in result:
        print(item.get_info())
