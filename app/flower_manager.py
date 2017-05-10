from flower_manager_storage import FlowerManagerStorage
from pymongo import MongoClient


class FlowerManager(object):
    def __init__(self):
        conn = MongoClient()
        db = conn['flower_db']
        mongodb_collection = db['flowers']
        self.flower_manager_store = FlowerManagerStorage(mongodb_collection)

    def get_flower_info(self, flower_name):
        return self.flower_manager_store.get_flower_intro_by_name(flower_name)
