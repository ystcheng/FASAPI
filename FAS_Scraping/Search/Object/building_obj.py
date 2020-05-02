from typing import *
import json


class BuildingObj:
    _id: str
    _code_name: str
    _name: str
    _address: str
    _postal_code: str

    def __init__(self, id: str, _code_name: str, name: str,
                 address: str, postal_code: str):
        self._id = id
        self._code_name = _code_name
        self._name = name
        self. _address = address
        self._postal_code = postal_code

    def get_info(self) -> Dict:
        result = {
            "id": self._id,
            "code": self._code_name,
            "name": self._name,
            "address": self._address,
            "postal": self._postal_code
        }

        return result
