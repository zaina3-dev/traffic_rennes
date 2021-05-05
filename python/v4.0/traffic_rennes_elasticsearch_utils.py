# coding: utf-8

import json
import time

import requests
from elasticsearch import Elasticsearch
from flask import flash

class Config():
    def __init__(self):
        self.index_name = "traffic_rennes"
        self.index_init = False
        self.traffic_nb_rows = 10
        self.traffic_reliability = 5
        self.traffic_time_interval = 5
        self.traffic_time_max = 15


def read_json():
    jsonFile = "param.json"
    try:
        with open(jsonFile) as f:
            file_data = json.load(f)
            f.close()
    except:
        file_data = Config.query.all()
        submission_successful = "could not read file"

    return file_data

# flash le contenu d'un json
def jflash(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)


def test():
    flash('--> test flash')


