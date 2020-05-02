from bs4 import BeautifulSoup
from typing import List
from Object.building_obj import BuildingObj

import requests
import json
import os


class BuildingSearch:
    _url: str

    def __init__(self):
        # path = os.path.dirname(os.path.abspath(__file__))
        # self._url = os.path.join(
        #     path, 'Testing\\buildingSearch.html'
        # )

        self._url = 'http://map.utoronto.ca/utsg/c/buildings'

    def building_search(self) -> List:
        result = []
        # soup = BeautifulSoup(open(self._url), 'html.parser')
        soup = BeautifulSoup(requests.get(self._url).text, 'html.parser')
        data = soup.find(attrs={'class': 'buildinglist'})
        buildingsoup = BeautifulSoup(str(data), 'html.parser')
        building_listings = buildingsoup.find_all('li')

        for building in building_listings:
            data = self._clean_building(
                building.getText(), BeautifulSoup(str(building), 'html.parser')
            )
            result.append(data.get_info())

        return result

    def _clean_building(self, building_text: str, idsoup: BeautifulSoup) -> BuildingObj:
        building_info = building_text.strip().split('\n')
        sub_info1 = building_info[0].split('|')
        sub_info2 = building_info[1].split(',')

        name = sub_info1[0].strip()
        code = sub_info1[1].strip()
        address = sub_info2[0].strip()
        if len(sub_info2) > 1:
            postal = sub_info2[1].strip()
        else:
            postal = ''

        data = idsoup.find('a', href=True)
        id = data['href'].split('/')[-1].strip()

        return BuildingObj(id, code, name, address, postal)

if __name__ == '__main__':
    test = BuildingSearch()
    print(json.dumps(test.building_search(), indent=2))

