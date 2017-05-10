
from flower_entities import FlowerInfo
from flower_exceptions import NameNotFoundException


class FlowerManagerStorage(object):
    def __init__(self, mongodb_collection):
        self._mongodb_collection = mongodb_collection

    def get_flower_intro_by_name(self, flower_name):
        flower_info_store = self._mongodb_collection.find_one({"name": flower_name})
        if flower_info_store is None:
            raise NameNotFoundException
        flower_info = FlowerInfo()
        flower_info.load(flower_info_store)
        return flower_info

