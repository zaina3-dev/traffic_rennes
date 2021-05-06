# coding: utf-8

import json
from elasticsearch import Elasticsearch


# test le port elasticsearch
def connect_elasticsearch(host, port):
    es = None
    es = Elasticsearch([{'host':host, 'port':port}])
    if es.ping():
        print('--> elasticsearch bien connecté')
        es._connected = True
    else:
        server = host +':'+ str(port) +'/'
        print('--> /!\\ elasticsearch pas de réponse :', server)
        es._connected = False
    return es


# print le contenu d'un json
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

