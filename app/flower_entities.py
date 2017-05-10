# -*- coding:utf-8 -*-
from __future__ import absolute_import, print_function
import pprint
from bson import ObjectId


class FlowerInfo(object):
    def __init__(self):
        self.flower_id = None
        self.flower_name = ""
        self.flower_intro = ""
        self.flower_lan = ""
        self.flower_medical = ""
        self.flower_video = ""

    def __str__(self):
        return pprint.pformat(self.dump())

    def get_flower_id(self):
        return self.flower_id

    def get_flower_name(self):
        return self.flower_name

    def get_flower_intro(self):
        return self.flower_intro

    def get_flower_lan(self):
        return self.flower_lan

    def get_flower_medical(self):
        return self.flower_medical

    def get_flower_video(self):
        return self.flower_video

    def set_flower_name(self, flower_name):
        self.flower_name = flower_name

    def set_flower_intro(self, flower_intro):
        self.flower_intro = flower_intro

    def set_flower_lan(self, flower_lan):
        self.flower_lan = flower_lan

    def set_flower_medical(self, flower_medical):
        self.flower_medical = flower_medical

    def dump(self):
        dumped_dict = {
            "_id": self.flower_id,
            "flower_name" : self.flower_name,
            "flower_intro": self.flower_intro,
            "flower_lan": self.flower_lan,
            "flower_medical": self.flower_medical,
            "flower_video": self.flower_video
        }
        return dumped_dict

    def load(self, flower_dict):
        self.flower_id = flower_dict["_id"]
        self.flower_name = flower_dict["flower_name"]
        self.flower_intro = flower_dict["flower_intro"]
        self.flower_lan = flower_dict["flower_lan"]
        self.flower_medical = flower_dict["flower_medical"]
        self.flower_video = flower_dict["flower_video"]

    def save(self, mongodb_collection):
        if self.flower_id is None:
            self.flower_id = ObjectId()
        flower_info_json = self.dump()
        mongodb_collection.save(flower_info_json)
