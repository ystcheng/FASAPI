from typing import *

import json


class CourseObj:
    _code: str
    _title: str
    _description: str
    _prerequisite: str
    _exclusion: str

    def __init__(self, code: str, title: str, description: str,
                 prerequisite: str, exclusion: str):
        self._code = code
        self._title = title
        self._description = description
        self._prerequisite = prerequisite
        self._exclusion = exclusion

    def get_info(self) -> Dict:
        result = {
            "code": self._code,
            "title": self._title,
            "description": self._description,
            "prerequisite": self._prerequisite,
            "exclusion": self._exclusion
        }

        return result
