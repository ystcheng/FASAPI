from pymongo import MongoClient
from typing import List
import json

class MongoAPI:

    def _init_api(self):
        self._client = MongoClient('localhost', 27017)
        self._db = self._client['FASAPI']

    def store(self, collection: str, post: json) -> int:
        self._init_api()
        col = self._db[collection]
        self._client.close()
        return col.insert_one(post).inserted_id

    # def get(self, collection: str) -> List[json]:
    #     self._init_api()
    #     col = self._db[collection]
    #     result = [json.dumps(document) for document in col.find()]
    #     return result

