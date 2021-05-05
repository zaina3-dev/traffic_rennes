# coding: utf-8

import json
from elasticsearch import Elasticsearch


# test le port elasticsearch
def connect_elasticsearch():
    es = None
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if es.ping():
        print('--> elasticsearch bien connecté')
        es._connected = True
    else:
        print('--> /!\\ elasticSearch pas de réponse')
        es._connected = False
    return es


# print le contenu d'un json
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

